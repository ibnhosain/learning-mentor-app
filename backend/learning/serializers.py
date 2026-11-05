from rest_framework import serializers
from .models import LessonProgress, Submission, Evaluation, SkillTracker, DailyLog


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = (
            'id', 'scores', 'total_score',
            'what_is_correct', 'what_is_wrong', 'hints',
            'next_step', 'status', 'evaluated_at',
        )


class SubmissionSerializer(serializers.ModelSerializer):
    evaluation = EvaluationSerializer(read_only=True)

    class Meta:
        model = Submission
        fields = ('id', 'lesson', 'code', 'explanation', 'submitted_at', 'evaluation')
        read_only_fields = ('submitted_at',)


class SubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ('code', 'explanation')


class ProgressSummarySerializer(serializers.Serializer):
    total_lessons = serializers.IntegerField()
    completed = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    needs_revision = serializers.IntegerField()
    not_started = serializers.IntegerField()
    overall_percent = serializers.FloatField()


class SkillTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillTracker
        fields = ('id', 'skill_name', 'level', 'last_updated')


class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = ('id', 'date', 'content', 'created_at')
