from rest_framework import serializers
from .models import Stage, Module, Lesson
from learning.models import LessonProgress


class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ('status', 'attempts', 'best_score', 'completed_at')


class LessonSerializer(serializers.ModelSerializer):
    progress = LessonProgressSerializer(read_only=True)
    stage_number = serializers.IntegerField(source='module.stage.number', read_only=True)
    stage_title = serializers.CharField(source='module.stage.title', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'id', 'title', 'day_number', 'content',
            'stage_number', 'stage_title', 'module_title',
            'progress',
        )


class LessonListSerializer(serializers.ModelSerializer):
    """Shorter version for lists — no full content."""
    progress = LessonProgressSerializer(read_only=True)
    stage_number = serializers.IntegerField(source='module.stage.number', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'day_number', 'stage_number', 'module_title', 'progress')


class ModuleSerializer(serializers.ModelSerializer):
    lessons = LessonListSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ('id', 'number', 'title', 'lessons')


class StageSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Stage
        fields = ('id', 'number', 'title', 'description', 'modules')
