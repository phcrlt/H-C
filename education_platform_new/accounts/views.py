from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group  # Добавляем импорт Group
from .forms import UserUpdateForm, ProfileUpdateForm  # Раскомментировать ProfileUpdateForm

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            try:
                # Создаем пользователя
                user = User.objects.create_user(username=username, email=email, password=password1)
                
                # АВТОМАТИЧЕСКИ ДОБАВЛЯЕМ В ГРУППУ STUDENTS
                try:
                    students_group = Group.objects.get(name='Students')
                    user.groups.add(students_group)
                    print(f"✅ Пользователь {username} добавлен в группу Students")  # Для отладки
                except Group.DoesNotExist:
                    print("⚠️ Группа Students не найдена")  # Для отладки
                
                # Логиним пользователя
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно! Вы добавлены в группу Students.')
                return redirect('home')
            except Exception as e:
                messages.error(request, f'Ошибка при создании пользователя: {str(e)}')
        else:
            messages.error(request, 'Пароли не совпадают')
    
    return render(request, 'registration/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы!')
    return redirect('home')

@login_required
def personal_cabinet(request):
    from core.models import Enrollment, Submission, Grade  # Добавляем импорты
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен!')
            return redirect('personal_cabinet')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    # Собираем статистику
    enrollments = Enrollment.objects.filter(user=request.user)
    submissions = Submission.objects.filter(student=request.user)
    grades = Grade.objects.filter(submission__student=request.user)
    
    # Основная статистика
    total_courses = enrollments.count()
    active_courses = enrollments.filter(completed=False).count()
    completed_courses = enrollments.filter(completed=True).count()
    
    # Подсчитываем общее время обучения (примерно)
    total_lessons = sum(enrollment.total_lessons_count() for enrollment in enrollments)
    completed_lessons = sum(enrollment.completed_lessons_count() for enrollment in enrollments)
    
    # Средний прогресс по всем курсам
    if enrollments.exists():
        avg_progress = sum(enrollment.progress_percentage() for enrollment in enrollments) // enrollments.count()
    else:
        avg_progress = 0
    
    # Статистика по заданиям
    total_assignments = submissions.count()
    graded_assignments = grades.count()
    
    # Средняя оценка
    if grades.exists():
        avg_grade = sum(grade.score for grade in grades) // grades.count()
    else:
        avg_grade = 0
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'total_courses': total_courses,
        'active_courses': active_courses,
        'completed_courses': completed_courses,
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'avg_progress': avg_progress,
        'total_assignments': total_assignments,
        'graded_assignments': graded_assignments,
        'avg_grade': avg_grade,
    }
    
    return render(request, 'profile/personal_cabinet.html', context)