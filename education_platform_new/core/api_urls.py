from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import CourseViewSet, LessonViewSet, AssignmentViewSet, SubmissionViewSet, GradeViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'grades', GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]