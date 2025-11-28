from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                    # Красивая главная
    path('simple/', views.home_simple, name='home_simple'),  # Простая главная
    path('courses/', views.courses_list, name='courses_list'),
]