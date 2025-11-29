from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'courses', api_views.CourseViewSet)
router.register(r'lessons', api_views.LessonViewSet)
router.register(r'assignments', api_views.AssignmentViewSet)
router.register(r'submissions', api_views.SubmissionViewSet)
router.register(r'grades', api_views.GradeViewSet)

urlpatterns = [
    path('', include(router.urls)),
        path('course-autocomplete/', api_views.course_autocomplete, name='course-autocomplete'),
]