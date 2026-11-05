from django.urls import path
from .views import StageListView, LessonListView, LessonDetailView

urlpatterns = [
    path('stages/', StageListView.as_view(), name='stage-list'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
]
