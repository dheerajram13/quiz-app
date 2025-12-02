from django.contrib import admin
from .models import Quiz, Question, Answer, UserQuizAttempt, Category, Tag


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'description']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ['text', 'is_correct', 'explanation', 'order']


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['text', 'quiz', 'question_type', 'points']
    list_filter = ['quiz', 'question_type']
    search_fields = ['text']


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    fields = ['question_type', 'text', 'points', 'order']


class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'category', 'difficulty_level', 'time_limit_minutes', 'is_active', 'created_at']
    list_filter = ['difficulty_level', 'category', 'is_active', 'tags']
    search_fields = ['title', 'description']
    filter_horizontal = ['tags']
    fields = ['title', 'description', 'category', 'tags', 'difficulty_level', 'time_limit_minutes', 'is_active']


class UserQuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'time_taken_seconds', 'completed_at']
    list_filter = ['quiz', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['answers_data', 'started_at', 'completed_at', 'time_taken_seconds']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserQuizAttempt, UserQuizAttemptAdmin)