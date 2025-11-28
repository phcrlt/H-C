from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, Lesson, Assignment, Submission, Grade, Comment
from .serializers import (
    CourseSerializer, LessonSerializer, AssignmentSerializer,
    SubmissionSerializer, GradeSerializer, CommentSerializer
)

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