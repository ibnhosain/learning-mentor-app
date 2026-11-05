import json
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from curriculum.models import Lesson
from .models import LessonProgress, Submission, Evaluation, DailyLog
from .serializers import (
    SubmissionSerializer, SubmissionCreateSerializer,
    EvaluationSerializer, ProgressSummarySerializer, DailyLogSerializer,
)
from ai_client import evaluate_submission, generate_daily_log


class TodayLessonView(APIView):
    """আজকের পাঠ — in_progress অথবা প্রথম not_started lesson।"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # in_progress lesson আছে কিনা দেখো
        in_progress = LessonProgress.objects.filter(
            status='in_progress'
        ).select_related('lesson__module__stage').first()

        if in_progress:
            lesson = in_progress.lesson
        else:
            # প্রথম not_started বা progress নেই এমন lesson
            all_lessons = Lesson.objects.order_by('day_number')
            lesson = None
            for l in all_lessons:
                prog, _ = LessonProgress.objects.get_or_create(lesson=l)
                if prog.status == 'not_started':
                    lesson = l
                    prog.status = 'in_progress'
                    prog.save()
                    break

        if not lesson:
            return Response({'message': 'সব পাঠ সম্পন্ন হয়েছে! অভিনন্দন!'})

        from curriculum.serializers import LessonSerializer
        return Response(LessonSerializer(lesson).data)


class SubmissionCreateView(APIView):
    """Lesson-এ code জমা দাও এবং AI মূল্যায়ন পাও।"""
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'পাঠ পাওয়া যায়নি।'}, status=status.HTTP_404_NOT_FOUND)

        # দৈনিক submission limit চেক
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = Submission.objects.filter(
            lesson=lesson,
            submitted_at__gte=today_start,
        ).count()
        if today_count >= settings.MAX_DAILY_SUBMISSIONS:
            return Response(
                {'error': f'আজকে সর্বোচ্চ {settings.MAX_DAILY_SUBMISSIONS}টি submission করা যাবে।'},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        serializer = SubmissionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        submission = Submission.objects.create(lesson=lesson, **serializer.validated_data)

        # AI মূল্যায়ন
        eval_data = evaluate_submission(lesson, submission)
        if eval_data is None:
            return Response(
                {'error': 'AI মূল্যায়ন করতে পারেনি। একটু পরে আবার চেষ্টা করো।'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        evaluation = Evaluation.objects.create(submission=submission, **eval_data)

        # Progress আপডেট
        progress, _ = LessonProgress.objects.get_or_create(lesson=lesson)
        progress.attempts += 1
        if evaluation.total_score > progress.best_score:
            progress.best_score = evaluation.total_score

        if evaluation.status == 'Completed' and evaluation.total_score >= 75:
            progress.status = 'completed'
            progress.completed_at = timezone.now()
        else:
            progress.status = 'needs_revision'
        progress.save()

        return Response(EvaluationSerializer(evaluation).data, status=status.HTTP_201_CREATED)


class SubmissionDetailView(APIView):
    """Submission ও তার Evaluation দেখো।"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            submission = Submission.objects.select_related('evaluation').get(pk=pk)
        except Submission.DoesNotExist:
            return Response({'error': 'পাওয়া যায়নি।'}, status=status.HTTP_404_NOT_FOUND)
        return Response(SubmissionSerializer(submission).data)


class ProgressView(APIView):
    """সামগ্রিক অগ্রগতির সারসংক্ষেপ।"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from curriculum.models import Lesson
        total = Lesson.objects.count()
        statuses = LessonProgress.objects.values_list('status', flat=True)
        status_map = {'completed': 0, 'in_progress': 0, 'needs_revision': 0, 'not_started': 0}
        for s in statuses:
            status_map[s] = status_map.get(s, 0) + 1
        status_map['not_started'] += total - LessonProgress.objects.count()

        data = {
            'total_lessons': total,
            'completed': status_map['completed'],
            'in_progress': status_map['in_progress'],
            'needs_revision': status_map['needs_revision'],
            'not_started': status_map['not_started'],
            'overall_percent': round(status_map['completed'] / total * 100, 1) if total else 0,
        }
        return Response(data)


class DailyLogGenerateView(APIView):
    """আজকের daily log তৈরি করো (AI দিয়ে)।"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        today = date.today()
        log, created = DailyLog.objects.get_or_create(date=today)
        if not created and not request.data.get('regenerate'):
            return Response(DailyLogSerializer(log).data)

        # আজকের submissions সংগ্রহ
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        submissions = Submission.objects.filter(
            submitted_at__gte=today_start
        ).select_related('lesson', 'evaluation')

        content = generate_daily_log(submissions)
        log.content = content
        log.save()
        return Response(DailyLogSerializer(log).data)
