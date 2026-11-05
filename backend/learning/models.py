from django.db import models
from curriculum.models import Lesson


class LessonProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('needs_revision', 'Needs Revision'),
        ('completed', 'Completed'),
    ]
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='progress')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    attempts = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Day {self.lesson.day_number} — {self.get_status_display()}"


class Submission(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions')
    code = models.TextField()
    explanation = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Submission for Day {self.lesson.day_number} at {self.submitted_at:%Y-%m-%d %H:%M}"


class Evaluation(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='evaluation')
    # scores: {"concept": 0-20, "independent_coding": 0-30, "debugging": 0-20, "project_quality": 0-20, "explanation": 0-10}
    scores = models.JSONField(default=dict)
    total_score = models.IntegerField(default=0)
    what_is_correct = models.JSONField(default=list)
    what_is_wrong = models.JSONField(default=list)
    hints = models.JSONField(default=list)
    next_step = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='In Progress')
    raw_response = models.TextField(blank=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation: {self.total_score}% — {self.status}"


class SkillTracker(models.Model):
    skill_name = models.CharField(max_length=200, unique=True)
    # 0=শেখা হয়নি, 1=শুনেছি, 2=বুঝি, 3=সাহায্য নিয়ে পারি, 4=নিজে পারি, 5=project-এ প্রয়োগ করতে পারি
    level = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.skill_name}: Level {self.level}"


class DailyLog(models.Model):
    date = models.DateField(unique=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Daily Log: {self.date}"
