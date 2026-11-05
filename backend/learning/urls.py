from django.urls import path
from .views import (
    TodayLessonView, SubmissionCreateView, SubmissionDetailView,
    ProgressView, DailyLogGenerateView,
)

urlpatterns = [
    path('today/', TodayLessonView.as_view(), name='today-lesson'),
    path('lessons/<int:lesson_id>/submissions/', SubmissionCreateView.as_view(), name='submission-create'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-detail'),
    path('progress/', ProgressView.as_view(), name='progress'),
    path('daily-log/generate/', DailyLogGenerateView.as_view(), name='daily-log-generate'),
]
