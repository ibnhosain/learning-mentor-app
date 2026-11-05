from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Stage, Lesson
from .serializers import StageSerializer, LessonSerializer, LessonListSerializer
from learning.models import LessonProgress


class StageListView(generics.ListAPIView):
    queryset = Stage.objects.prefetch_related('modules__lessons__progress').all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]


class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.select_related('module__stage').prefetch_related('progress').all()
    serializer_class = LessonListSerializer
    permission_classes = [IsAuthenticated]


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.select_related('module__stage').prefetch_related('progress').all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
