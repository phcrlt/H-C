from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Course, Lesson, Assignment, Submission, Grade, Comment

class Command(BaseCommand):
    help = 'Создает группы Teachers и Students с соответствующими правами'
    
    def handle(self, *args, **options):
        # Создаем или получаем группы
        teachers_group, created_teachers = Group.objects.get_or_create(name='Teachers')
        students_group, created_students = Group.objects.get_or_create(name='Students')
        
        # Очищаем существующие права (для чистоты)
        teachers_group.permissions.clear()
        students_group.permissions.clear()
        
        # Получаем ContentType для наших моделей
        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)
        assignment_ct = ContentType.objects.get_for_model(Assignment)
        submission_ct = ContentType.objects.get_for_model(Submission)
        grade_ct = ContentType.objects.get_for_model(Grade)
        comment_ct = ContentType.objects.get_for_model(Comment)
        
        # Собираем все permissions для наших моделей
        course_perms = Permission.objects.filter(content_type=course_ct)
        lesson_perms = Permission.objects.filter(content_type=lesson_ct)
        assignment_perms = Permission.objects.filter(content_type=assignment_ct)
        submission_perms = Permission.objects.filter(content_type=submission_ct)
        grade_perms = Permission.objects.filter(content_type=grade_ct)
        comment_perms = Permission.objects.filter(content_type=comment_ct)
        
        # Назначаем права для TEACHERS (полный доступ)
        teacher_permissions = [
            *course_perms,      # Может создавать, редактировать, удалять курсы
            *lesson_perms,      # Может создавать, редактировать, удалять уроки
            *assignment_perms,  # Может создавать, редактировать, удалять задания
            *submission_perms,  # Может просматривать все сдачи
            *grade_perms,       # Может выставлять оценки
            *comment_perms,     # Может комментировать
        ]
        
        for perm in teacher_permissions:
            teachers_group.permissions.add(perm)
        
        # Назначаем права для STUDENTS (ограниченный доступ)
        student_permissions = [
            # Может только просматривать курсы, уроки, задания
            *course_perms.filter(codename__in=['view_course']),
            *lesson_perms.filter(codename__in=['view_lesson']),
            *assignment_perms.filter(codename__in=['view_assignment']),
            # Может создавать сдачи и комментарии
            *submission_perms.filter(codename__in=['view_submission', 'add_submission']),
            *comment_perms.filter(codename__in=['view_comment', 'add_comment']),
            # Может просматривать свои оценки
            *grade_perms.filter(codename__in=['view_grade']),
        ]
        
        for perm in student_permissions:
            students_group.permissions.add(perm)
        
        # Выводим результаты
        if created_teachers:
            self.stdout.write(
                self.style.SUCCESS('✅ Группа Teachers создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Группа Teachers уже существует')
            )
            
        if created_students:
            self.stdout.write(
                self.style.SUCCESS('✅ Группа Students создана')
            )
        else:
            self.stdout.write(
                self.style.WARNING('ℹ️ Группа Students уже существует')
            )
        
        self.stdout.write(
            self.style.SUCCESS(f'🎯 Назначено прав для Teachers: {len(teacher_permissions)}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🎓 Назначено прав для Students: {len(student_permissions)}')
        )
        
        self.stdout.write(
            self.style.SUCCESS('🎉 Группы успешно инициализированы!')
        )