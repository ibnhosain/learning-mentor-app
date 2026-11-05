from django.contrib import admin
from .models import LessonProgress, Submission, Evaluation, SkillTracker, DailyLog


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'status', 'attempts', 'best_score', 'completed_at')
    list_filter = ('status',)


class EvaluationInline(admin.StackedInline):
    model = Evaluation
    extra = 0
    readonly_fields = ('total_score', 'scores', 'status', 'evaluated_at')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'submitted_at')
    list_filter = ('lesson__module__stage',)
    inlines = [EvaluationInline]


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('submission', 'total_score', 'status', 'evaluated_at')
    list_filter = ('status',)
    readonly_fields = ('raw_response',)


@admin.register(SkillTracker)
class SkillTrackerAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'level', 'last_updated')


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'created_at')
    ordering = ('-date',)
