from django.contrib import admin
from .models import Stage, Module, Lesson


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0
    fields = ('day_number', 'title', 'is_seeded', 'order')
    readonly_fields = ('day_number',)


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'order')
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('stage', 'number', 'title', 'order')
    list_filter = ('stage',)
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('day_number', 'title', 'module', 'is_seeded', 'created_at')
    list_filter = ('module__stage', 'is_seeded')
    search_fields = ('title', 'content')
    ordering = ('day_number',)
