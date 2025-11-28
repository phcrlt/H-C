from rest_framework import serializers
from .models import Course, Lesson, Assignment, Submission, Grade, Comment
from django.contrib.auth.models import User

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'duration', 'course']

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'short_description', 
            'image', 'duration', 'level', 'price', 'is_free',
            'created_at', 'updated_at', 'lessons', 'lessons_count'
        ]
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()
    
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_name', 'text', 'created_at', 'is_teacher_comment']

class GradeSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.username', read_only=True)
    
    class Meta:
        model = Grade
        fields = ['id', 'teacher', 'teacher_name', 'score', 'feedback', 'graded_at']

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.username', read_only=True)
    grade = GradeSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Submission
        fields = [
            'id', 'assignment', 'student', 'student_name', 'file', 
            'text', 'submitted_at', 'grade', 'comments'
        ]

class AssignmentSerializer(serializers.ModelSerializer):
    submissions = SubmissionSerializer(many=True, read_only=True)
    submissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'lesson', 'title', 'description', 'created_at',
            'updated_at', 'deadline', 'max_score', 'submissions', 'submissions_count'
        ]
    
    def get_submissions_count(self, obj):
        return obj.submissions.count()

# Обновим LessonSerializer чтобы включить задания
class LessonSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'order', 'duration', 'course', 'assignments']    