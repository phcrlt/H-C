from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('courses/', views.courses_list, name='courses_list'),
    path('lessons/', views.lessons_list, name='lessons_list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('assignments/', views.assignments_list, name='assignments_list'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
]