from django.contrib import admin
from .models import Course, Lesson, Assignment, Submission, Grade, Comment, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'is_free', 'duration', 'created_at', 'enrollments_count']
    list_filter = ['level', 'is_free', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'short_description', 'description', 'image')
        }),
        ('Детали', {
            'fields': ('level', 'duration', 'price', 'is_free')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def enrollments_count(self, obj):
        return obj.enrollments.count()
    enrollments_count.short_description = 'Записей'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration', 'assignments_count']
    list_filter = ['course']  # УБРАЛ 'created_at' - его нет в модели
    search_fields = ['title', 'content']
    ordering = ['course', 'order']
    
    def assignments_count(self, obj):
        return obj.assignments.count()
    assignments_count.short_description = 'Заданий'

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'max_score', 'deadline', 'submissions_count']
    list_filter = ['lesson__course', 'created_at']
    search_fields = ['title', 'description']
    
    def submissions_count(self, obj):
        return obj.submissions.count()
    submissions_count.short_description = 'Сдач'

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_at', 'has_grade', 'grade_score']
    list_filter = ['assignment__lesson__course', 'submitted_at']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['submitted_at']
    
    def has_grade(self, obj):
        return obj.grade is not None
    has_grade.short_description = 'Оценено'
    has_grade.boolean = True
    
    def grade_score(self, obj):
        return obj.grade.score if obj.grade else '-'
    grade_score.short_description = 'Оценка'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['submission', 'teacher', 'score', 'graded_at']
    list_filter = ['teacher', 'graded_at']
    search_fields = ['submission__student__username', 'feedback']
    readonly_fields = ['graded_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'submission', 'is_teacher_comment', 'created_at']
    list_filter = ['is_teacher_comment', 'created_at']
    search_fields = ['author__username', 'text']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'completed', 'completed_at']
    list_filter = ['course', 'completed', 'enrolled_at']
    search_fields = ['user__username', 'course__title']
    readonly_fields = ['enrolled_at']