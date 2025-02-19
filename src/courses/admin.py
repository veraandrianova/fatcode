from django.contrib import admin
from . import models


class LessonTabInlines(admin.TabularInline):
    model = models.Lesson
    extra = 1


class QuizTabular(admin.TabularInline):
    model = models.Quiz
    extra = 1


class CodeTabular(admin.TabularInline):
    model = models.CodeQuestion
    extra = 1


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonTabInlines]
    list_display = ('name', 'author', 'mentor')
    ordering = ['published']
    prepopulated_fields = {"slug": ("name",)}

    class Meta:
        fields = '__all__'


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [QuizTabular, CodeTabular]
    list_display = ('id', 'course', 'lesson_type')

    class Meta:
        fields = '__all__'


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('name', 'parent')


admin.site.register(models.Tag)
