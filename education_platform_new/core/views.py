from django.shortcuts import render
from .models import Course

def home(request):
    # КРАСИВАЯ главная страница по умолчанию
    courses = Course.objects.all()[:6]
    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)

def home_simple(request):
    # Простая главная страница
    return render(request, 'index_simple.html')

def courses_list(request):
    # Страница всех курсов
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'courses/courses_list.html', context)