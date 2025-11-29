from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from core.models import Course, Lesson, Assignment

class Command(BaseCommand):
    help = 'Создает тестовые данные для демонстрации'
    
    def handle(self, *args, **options):
        # Создаем тестового преподавателя
        teacher, created = User.objects.get_or_create(
            username='teacher1',
            defaults={
                'email': 'teacher@example.com',
                'first_name': 'Иван',
                'last_name': 'Преподавателей'
            }
        )
        if created:
            teacher.set_password('password123')
            teacher.save()
            teachers_group = Group.objects.get(name='Teachers')
            teacher.groups.add(teachers_group)
            self.stdout.write(self.style.SUCCESS('✅ Тестовый преподаватель создан'))
        
        # Создаем тестового студента
        student, created = User.objects.get_or_create(
            username='student1',
            defaults={
                'email': 'student@example.com',
                'first_name': 'Петр',
                'last_name': 'Студентов'
            }
        )
        if created:
            student.set_password('password123')
            student.save()
            students_group = Group.objects.get(name='Students')
            student.groups.add(students_group)
            self.stdout.write(self.style.SUCCESS('✅ Тестовый студент создан'))
        
        # Создаем тестовый курс
        course, created = Course.objects.get_or_create(
            title='Python для начинающих',
            defaults={
                'short_description': 'Изучите основы программирования на Python',
                'description': 'Подробный курс по основам программирования на языке Python. Идеально для новичков.',
                'duration': '4 недели',
                'level': 'beginner',
                'is_free': True,
                'price': 0
            }
        )
        
        if created:
            # Создаем уроки для курса
            lesson1 = Lesson.objects.create(
                course=course,
                title='Введение в Python',
                content='Основные концепции и синтаксис Python...',
                order=1,
                duration=60
            )
            
            lesson2 = Lesson.objects.create(
                course=course,
                title='Переменные и типы данных',
                content='Работа с переменными, строками, числами...',
                order=2,
                duration=45
            )
            
            # Создаем задание для первого урока
            assignment = Assignment.objects.create(
                lesson=lesson1,
                title='Первая программа на Python',
                description='Напишите программу, которая выводит "Hello, World!"',
                max_score=100
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Тестовый курс создан с уроками и заданиями'))
        
        self.stdout.write(self.style.SUCCESS('🎉 Тестовые данные успешно созданы!'))
        self.stdout.write('👨‍🏫 Преподаватель: teacher1 / password123')
        self.stdout.write('👨‍🎓 Студент: student1 / password123')