from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lesson, Assignment, Submission, Grade, Comment
from .serializers import (
    CourseSerializer, LessonSerializer, AssignmentSerializer,
    SubmissionSerializer, GradeSerializer, CommentSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import models 
class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def lessons(self, request, pk=None):
        course = self.get_object()
        lessons = course.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # ДОБАВЛЯЕМ queryset атрибут для роутера
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Teachers').exists():
            return Submission.objects.all()
        return Submission.objects.filter(student=user)
    
    # Определяем базовый queryset для роутера
    queryset = Submission.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(student=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        submission = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                submission=submission,
                author=request.user,
                is_teacher_comment=request.user.groups.filter(name='Teachers').exists()
            )
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def grade(self, request, pk=None):
        submission = self.get_object()
        
        # Проверяем что пользователь - преподаватель
        if not request.user.groups.filter(name='Teachers').exists():
            return Response(
                {'error': 'Только преподаватели могут выставлять оценки'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            # Удаляем старую оценку если есть
            Grade.objects.filter(submission=submission).delete()
            serializer.save(submission=submission, teacher=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GradeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Teachers').exists():
            return Grade.objects.all()
        return Grade.objects.filter(submission__student=user)
    
    # Определяем базовый queryset для роутера
    queryset = Grade.objects.all()
    
@api_view(['GET'])
def course_autocomplete(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return Response([])
    
    courses = Course.objects.filter(
        models.Q(title__icontains=query) |
        models.Q(short_description__icontains=query)
    )[:10]  # Ограничиваем 10 результатами
    
    suggestions = [
        {
            'id': course.id,
            'title': course.title,
            'short_description': course.short_description,
            'level': course.get_level_display(),
            'is_free': course.is_free
        }
        for course in courses
    ]
    
    return Response(suggestions)