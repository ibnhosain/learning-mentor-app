import io
import json
import zipfile
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from curriculum.models import Lesson
from .models import LessonProgress, Submission, Evaluation, DailyLog
from .serializers import (
    SubmissionSerializer, SubmissionCreateSerializer,
    EvaluationSerializer, ProgressSummarySerializer, DailyLogSerializer,
)
from ai_client import evaluate_submission, evaluate_any_file, generate_daily_log

MAX_FILE_SIZE = 10 * 1024 * 1024   # 10 MB
MAX_FILE_CHARS = 4000               # text হলে prompt-এ এতটুকুই পাঠাবো
MAX_ZIP_SIZE = 10 * 1024 * 1024

# এই extension-গুলো সরাসরি text হিসেবে পড়া যাবে
TEXT_EXTENSIONS = {
    '.html', '.htm', '.css', '.js', '.ts', '.jsx', '.tsx',
    '.py', '.txt', '.md', '.json', '.xml', '.svg', '.yaml',
    '.yml', '.java', '.c', '.cpp', '.cs', '.php', '.rb',
    '.go', '.rs', '.sh', '.sql', '.r', '.swift', '.kt',
}


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
    """সামগ্রিক অগ্রগতির সারসংক্ষেপ — দুর্বলতার তালিকাসহ।"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from curriculum.models import Lesson
        total = Lesson.objects.count()
        statuses = LessonProgress.objects.values_list('status', flat=True)
        status_map = {'completed': 0, 'in_progress': 0, 'needs_revision': 0, 'not_started': 0}
        for s in statuses:
            status_map[s] = status_map.get(s, 0) + 1
        status_map['not_started'] += total - LessonProgress.objects.count()

        # দুর্বলতার তালিকা — needs_revision lesson-গুলো
        weak = LessonProgress.objects.filter(
            status='needs_revision'
        ).select_related('lesson').order_by('lesson__day_number')
        weak_lessons = [
            {
                'id': p.lesson.id,
                'day_number': p.lesson.day_number,
                'title': p.lesson.title,
                'best_score': p.best_score,
                'attempts': p.attempts,
            }
            for p in weak
        ]

        data = {
            'total_lessons': total,
            'completed': status_map['completed'],
            'in_progress': status_map['in_progress'],
            'needs_revision': status_map['needs_revision'],
            'not_started': status_map['not_started'],
            'overall_percent': round(status_map['completed'] / total * 100, 1) if total else 0,
            'weak_lessons': weak_lessons,
        }
        return Response(data)


class AnyFileSubmissionView(APIView):
    """যেকোনো ফাইল জমা দিয়ে AI মূল্যায়ন পাও।"""
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({'error': 'পাঠ পাওয়া যায়নি।'}, status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'ফাইল দাও।'}, status=status.HTTP_400_BAD_REQUEST)
        if file.size > MAX_FILE_SIZE:
            return Response({'error': 'ফাইল ১০ MB-এর বেশি হওয়া যাবে না।'}, status=status.HTTP_400_BAD_REQUEST)

        explanation = request.data.get('explanation', '').strip()
        if not explanation:
            return Response({'error': 'নিজের ব্যাখ্যা লিখতে হবে।'}, status=status.HTTP_400_BAD_REQUEST)

        # Daily limit চেক
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_count = Submission.objects.filter(lesson=lesson, submitted_at__gte=today_start).count()
        if today_count >= settings.MAX_DAILY_SUBMISSIONS:
            return Response(
                {'error': f'আজকে সর্বোচ্চ {settings.MAX_DAILY_SUBMISSIONS}টি submission করা যাবে।'},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        filename = file.name
        ext = ('.' + filename.rsplit('.', 1)[-1].lower()) if '.' in filename else ''
        file_bytes = file.read()

        # ZIP হলে extract করে text হিসেবে পাঠাও
        if ext == '.zip':
            try:
                combined_code = _extract_zip_bytes(file_bytes)
            except Exception as e:
                return Response({'error': f'ZIP পড়া যায়নি: {e}'}, status=status.HTTP_400_BAD_REQUEST)
            submission = Submission.objects.create(lesson=lesson, code=combined_code[:8000], explanation=explanation)
            eval_data = evaluate_submission(lesson, submission)

        # Text file হলে সরাসরি prompt-এ পাঠাও
        elif ext in TEXT_EXTENSIONS:
            code = file_bytes.decode('utf-8', errors='ignore')[:MAX_FILE_CHARS * 2]
            submission = Submission.objects.create(lesson=lesson, code=code, explanation=explanation)
            eval_data = evaluate_submission(lesson, submission)

        # Binary file (image, PDF, audio, video) — Gemini File API
        else:
            submission = Submission.objects.create(
                lesson=lesson,
                code=f'[Binary file: {filename}]',
                explanation=explanation,
            )
            eval_data = evaluate_any_file(lesson, file_bytes, filename, explanation)

        if eval_data is None:
            return Response({'error': 'AI মূল্যায়ন করতে পারেনি।'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        evaluation = Evaluation.objects.create(submission=submission, **eval_data)

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


def _extract_zip_bytes(file_bytes):
    """ZIP থেকে text ফাইল পড়ে একটা string বানাও।"""
    result = []
    with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
        names = [n for n in z.namelist() if not n.startswith('__MACOSX') and not n.endswith('/')]
        names.sort()
        for name in names:
            ext = ('.' + name.rsplit('.', 1)[-1].lower()) if '.' in name else ''
            if ext not in TEXT_EXTENSIONS:
                continue
            with z.open(name) as f:
                content = f.read().decode('utf-8', errors='ignore')[:MAX_FILE_CHARS]
                result.append(f"=== {name} ===\n{content}")
    return '\n\n'.join(result)


class DailyLogGenerateView(APIView):
    """আজকের daily log তৈরি করো (AI দিয়ে) ও download করো।"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """আজকের log download করো (Markdown)।"""
        from django.http import HttpResponse
        today = date.today()
        log = DailyLog.objects.filter(date=today).first()
        if not log or not log.content:
            content = f"# Daily Log — {today}\n\nআজকে কোনো পাঠ সম্পন্ন হয়নি।\n"
        else:
            content = log.content
        response = HttpResponse(content, content_type='text/markdown; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="daily-log-{today}.md"'
        return response

    def post(self, request):
        today = date.today()
        log, created = DailyLog.objects.get_or_create(date=today)
        if not created and not request.data.get('regenerate'):
            return Response(DailyLogSerializer(log).data)

        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        submissions = Submission.objects.filter(
            submitted_at__gte=today_start
        ).select_related('lesson', 'evaluation')

        content = generate_daily_log(submissions)
        log.content = content
        log.save()
        return Response(DailyLogSerializer(log).data)
