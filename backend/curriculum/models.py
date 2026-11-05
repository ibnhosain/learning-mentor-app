from django.db import models


class Stage(models.Model):
    number = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Stage {self.number}: {self.title}"


class Module(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name='modules')
    number = models.IntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('stage', 'number')

    def __str__(self):
        return f"Stage {self.stage.number} Module {self.number}: {self.title}"


class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    day_number = models.IntegerField(unique=True)
    content = models.TextField()
    is_seeded = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['day_number']

    def __str__(self):
        return f"Day {self.day_number:02d}: {self.title}"
