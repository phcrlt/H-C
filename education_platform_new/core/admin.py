from django.contrib import admin
from .models import Course, Lesson, Assignment, Submission, Grade, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'is_free', 'price', 'created_at']
    list_filter = ['level', 'is_free', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration']
    list_filter = ['course']
    search_fields = ['title', 'content']
    ordering = ['course', 'order']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'max_score', 'deadline', 'created_at']
    list_filter = ['lesson__course', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['assignment', 'student', 'submitted_at', 'has_grade']
    list_filter = ['assignment__lesson__course', 'submitted_at']
    search_fields = ['student__username', 'assignment__title']
    readonly_fields = ['submitted_at']
    
    def has_grade(self, obj):
        return hasattr(obj, 'grade')
    has_grade.boolean = True
    has_grade.short_description = 'Оценка'

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['submission', 'teacher', 'score', 'graded_at']
    list_filter = ['teacher', 'graded_at']
    search_fields = ['submission__student__username', 'teacher__username']
    readonly_fields = ['graded_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'submission', 'created_at', 'is_teacher_comment']
    list_filter = ['is_teacher_comment', 'created_at']
    search_fields = ['author__username', 'text']
    readonly_fields = ['created_at']

# Создадим тестовые данные автоматически
def create_test_data():
    # Проверяем, есть ли уже курсы
    if not Course.objects.exists():
        print("Создаем тестовые данные...")
        
        # Создаем курсы
        python_course = Course.objects.create(
            title="Python для начинающих",
            short_description="Основы программирования на Python",
            description="Полный курс по основам программирования на Python для начинающих. Изучите синтаксис, структуры данных и основы ООП.",
            duration="6 недель",
            level="beginner",
            is_free=True,
            price=0
        )
        
        django_course = Course.objects.create(
            title="Веб-разработка на Django",
            short_description="Создание веб-приложений с Django",
            description="Научитесь создавать современные веб-приложения с использованием Django. REST API, аутентификация, базы данных.",
            duration="8 недель",
            level="intermediate", 
            is_free=False,
            price=2990
        )
        
        # Создаем уроки для Python курса
        lesson1 = Lesson.objects.create(
            course=python_course,
            title="Введение в Python",
            content="Основы синтаксиса Python, переменные, типы данных.",
            order=1,
            duration=45
        )
        
        lesson2 = Lesson.objects.create(
            course=python_course,
            title="Функции и модули", 
            content="Создание функций, импорт модулей, работа с аргументами.",
            order=2,
            duration=60
        )
        
        # Создаем уроки для Django курса
        lesson3 = Lesson.objects.create(
            course=django_course,
            title="Знакомство с Django",
            content="Установка Django, создание первого проекта, структура приложения.",
            order=1,
            duration=60
        )
        
        # Создаем задания
        assignment1 = Assignment.objects.create(
            lesson=lesson1,
            title="Первая программа на Python",
            description="Напишите программу, которая выводит 'Hello, World!' и выполняет базовые арифметические операции.",
            max_score=100
        )
        
        assignment2 = Assignment.objects.create(
            lesson=lesson2,
            title="Калькулятор функций",
            description="Создайте калькулятор с использованием функций для основных математических операций.",
            max_score=100
        )
        
        assignment3 = Assignment.objects.create(
            lesson=lesson3, 
            title="Первое Django приложение",
            description="Создайте простое Django приложение с одной страницей и базовой маршрутизацией.",
            max_score=100
        )
        
        print("Тестовые данные созданы!")
        print(f"- Курсы: {Course.objects.count()}")
        print(f"- Уроки: {Lesson.objects.count()}")
        print(f"- Задания: {Assignment.objects.count()}")

# Вызываем создание тестовых данных при запуске
create_test_data()