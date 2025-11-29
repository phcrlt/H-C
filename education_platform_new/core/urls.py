from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # Курсы
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('courses/<int:course_id>/unenroll/', views.unenroll_course, name='unenroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
    
    # Уроки
    path('lessons/', views.lessons_list, name='lessons_list'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    
    # Задания
    path('assignments/', views.assignments_list, name='assignments_list'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
]