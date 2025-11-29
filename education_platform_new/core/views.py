from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.db import models
from django.contrib.auth.models import User, Group 
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .models import Course, Lesson, Assignment, Submission, Grade, Comment, Enrollment  # Добавили Enrollment

def teacher_required(view_func):
    """Декоратор для проверки прав преподавателя"""
    def wrapper(request, *args, **kwargs):
        if not request.user.groups.filter(name='Teachers').exists():
            raise PermissionDenied("Доступ только для преподавателей")
        return view_func(request, *args, **kwargs)
    return wrapper

def home(request):
    courses = Course.objects.all()[:6]
    total_courses = Course.objects.count()
    total_students = User.objects.filter(groups__name='Students').count()
    total_teachers = User.objects.filter(groups__name='Teachers').count()
    
    context = {
        'courses': courses,
        'total_courses': total_courses,
        'total_students': total_students,
        'total_teachers': total_teachers,
    }
    return render(request, 'index.html', context)

def courses_list(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'courses/courses_list.html', context)

@login_required
def lessons_list(request):
    course_id = request.GET.get('course')
    
    if course_id:
        lessons = Lesson.objects.select_related('course').filter(course_id=course_id)
        course = get_object_or_404(Course, id=course_id)
    else:
        lessons = Lesson.objects.select_related('course').all()
        course = None
    
    # Получаем все курсы для фильтра
    courses = Course.objects.all()
    
    context = {
        'lessons': lessons,
        'selected_course': course,
        'courses': courses
    }
    return render(request, 'lessons/lessons_list.html', context)

@login_required
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    assignments = lesson.assignments.all()
    context = {
        'lesson': lesson,
        'assignments': assignments
    }
    return render(request, 'lessons/lesson_detail.html', context)

@login_required
def assignments_list(request):
    assignments = Assignment.objects.select_related('lesson', 'lesson__course').all()
    
    # Получаем сдачи текущего пользователя
    user_submissions = Submission.objects.filter(student=request.user)
    submitted_assignments = {sub.assignment_id for sub in user_submissions}
    
    context = {
        'assignments': assignments,
        'submitted_assignments': submitted_assignments
    }
    return render(request, 'assignments/assignments_list.html', context)

@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    
    # Получаем сдачу текущего пользователя
    user_submission = Submission.objects.filter(assignment=assignment, student=request.user).first()
    
    context = {
        'assignment': assignment,
        'user_submission': user_submission
    }
    return render(request, 'assignments/assignment_detail.html', context)

@login_required
def submit_assignment(request, assignment_id):
    """Сдача задания студентом"""
    try:
        assignment = get_object_or_404(Assignment, id=assignment_id)
        
        if request.method == 'POST':
            # Проверяем, не сдавал ли уже пользователь это задание
            existing_submission = Submission.objects.filter(
                assignment=assignment, 
                student=request.user
            ).first()
            
            if existing_submission:
                messages.error(request, 'Вы уже сдали эту работу!')
                return redirect('assignment_detail', assignment_id=assignment_id)
            
            # Получаем данные формы
            file = request.FILES.get('file')
            text = request.POST.get('text', '')
            
            # Проверяем что хотя бы что-то заполнено
            if not file and not text.strip():
                messages.error(request, 'Пожалуйста, загрузите файл или напишите текст ответа')
                return redirect('assignment_detail', assignment_id=assignment_id)
            
            # Создаем новую сдачу
            submission = Submission.objects.create(
                assignment=assignment,
                student=request.user,
                file=file if file else None,
                text=text
            )
            
            messages.success(request, 'Работа успешно сдана на проверку!')
            return redirect('assignment_detail', assignment_id=assignment_id)
        
        # Если GET запрос - перенаправляем на страницу задания
        return redirect('assignment_detail', assignment_id=assignment_id)
        
    except Exception as e:
        print(f"Error in submit_assignment: {e}")
        messages.error(request, f'Ошибка при отправке работы: {str(e)}')
        return redirect('assignment_detail', assignment_id=assignment_id)

def your_view(request):
    courses = Course.objects.all()
    total_assignments = sum(course.assignments.count() for course in courses)
    
    context = {
        'courses': courses,
        'total_assignments': total_assignments,
    }
    return render(request, 'teacher/courses.html', context)

def courses_list(request):
    search_query = request.GET.get('search', '')
    
    courses = Course.objects.all()
    
    if search_query:
        courses = courses.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(short_description__icontains=search_query)
        )
    
    context = {
        'courses': courses,
        'search_query': search_query
    }
    return render(request, 'courses/courses_list.html', context)

def courses_list(request):
    search_query = request.GET.get('search', '')
    level_filter = request.GET.get('level', '')
    type_filter = request.GET.get('type', '')
    
    courses = Course.objects.all()
    
    # Поиск
    if search_query:
        courses = courses.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(short_description__icontains=search_query)
        )
    
    # Фильтрация по уровню
    if level_filter:
        courses = courses.filter(level=level_filter)
    
    # Фильтрация по типу (бесплатные/премиум)
    if type_filter:
        if type_filter == 'free':
            courses = courses.filter(is_free=True)
        elif type_filter == 'premium':
            courses = courses.filter(is_free=False)
    
    # Получаем количество курсов по каждому фильтру для отображения
    total_courses = Course.objects.count()
    free_courses = Course.objects.filter(is_free=True).count()
    premium_courses = Course.objects.filter(is_free=False).count()
    
    level_counts = {
        'beginner': Course.objects.filter(level='beginner').count(),
        'intermediate': Course.objects.filter(level='intermediate').count(),
        'advanced': Course.objects.filter(level='advanced').count(),
    }
    
    context = {
        'courses': courses,
        'search_query': search_query,
        'level_filter': level_filter,
        'type_filter': type_filter,
        'total_courses': total_courses,
        'free_courses': free_courses,
        'premium_courses': premium_courses,
        'level_counts': level_counts,
    }
    return render(request, 'courses/courses_list.html', context)

@login_required
def enroll_course(request, course_id):
    """Запись пользователя на курс"""
    try:
        course = get_object_or_404(Course, id=course_id)
        
        # Проверяем, не записан ли уже пользователь
        existing_enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        
        if existing_enrollment:
            messages.info(request, f'Вы уже записаны на курс "{course.title}"')
        else:
            # Создаем запись
            Enrollment.objects.create(user=request.user, course=course)
            messages.success(request, f'Вы успешно записались на курс "{course.title}"!')
        
        return redirect('course_detail', course_id=course_id)
    except Exception as e:
        print(f"Error in enroll_course: {e}")  # Для отладки
        messages.error(request, 'Ошибка при записи на курс')
        return redirect('courses_list')

@login_required
def unenroll_course(request, course_id):
    """Отмена записи на курс"""
    try:
        course = get_object_or_404(Course, id=course_id)
        enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
        
        if enrollment:
            enrollment.delete()
            messages.success(request, f'Вы отписались от курса "{course.title}"')
        else:
            messages.error(request, 'Вы не были записаны на этот курс')
        
        return redirect('courses_list')
    except Exception as e:
        print(f"Error in unenroll_course: {e}")  # Для отладки
        messages.error(request, 'Ошибка при отписке от курса')
        return redirect('courses_list')

@login_required
def my_courses(request):
    """Страница 'Мои курсы' пользователя"""
    try:
        enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
        
        # Группируем по статусу
        active_courses = [e for e in enrollments if not e.completed]
        completed_courses = [e for e in enrollments if e.completed]
        
        context = {
            'active_courses': active_courses,
            'completed_courses': completed_courses,
            'total_courses': enrollments.count(),
        }
        return render(request, 'courses/my_courses.html', context)
    except Exception as e:
        print(f"Error in my_courses: {e}")  # Для отладки
        messages.error(request, 'Ошибка при загрузке ваших курсов')
        return redirect('home')

def course_detail(request, course_id):
    """Детальная страница курса с информацией о записи"""
    try:
        course = get_object_or_404(Course, id=course_id)
        lessons = course.lessons.all()
        
        # Проверяем записан ли пользователь на курс
        is_enrolled = False
        user_enrollment = None
        
        if request.user.is_authenticated:
            user_enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
            is_enrolled = user_enrollment is not None
        
        context = {
            'course': course,
            'lessons': lessons,
            'is_enrolled': is_enrolled,
            'user_enrollment': user_enrollment,
        }
        return render(request, 'courses/course_detail.html', context)
    except Exception as e:
        print(f"Error in course_detail: {e}")  # Для отладки
        messages.error(request, 'Ошибка при загрузке страницы курса')
        return redirect('courses_list')
    
@login_required
@teacher_required
def teacher_dashboard(request):
    """Дашборд преподавателя"""
    print("DEBUG: teacher_dashboard called")  # Отладка
    
    # Статистика преподавателя
    courses_taught = Course.objects.all()
    total_students = Enrollment.objects.filter(course__in=courses_taught).values('user').distinct().count()
    pending_submissions = Submission.objects.filter(grade__isnull=True).count()
    graded_count = Submission.objects.filter(grade__isnull=False).count()
    
    # Последние сдачи на проверку
    recent_submissions = Submission.objects.filter(grade__isnull=True).select_related(
        'student', 'assignment', 'assignment__lesson', 'assignment__lesson__course'
    )[:10]
    
    context = {
        'courses_taught': courses_taught,
        'total_students': total_students,
        'pending_submissions': pending_submissions,
        'graded_count': graded_count,
        'recent_submissions': recent_submissions,
        'total_courses': courses_taught.count(),
    }
    
    print(f"DEBUG: Context: {context}")  # Отладка
    return render(request, 'teacher/dashboard.html', context)

@login_required
@teacher_required
def teacher_courses(request):
    """Управление курсами преподавателя"""
    courses = Course.objects.all()  # Пока все курсы
    
    context = {
        'courses': courses,
    }
    return render(request, 'teacher/courses.html', context)

@login_required
@teacher_required
def teacher_submissions(request):
    """Список работ на проверку"""
    submissions = Submission.objects.select_related(
        'student', 'assignment', 'assignment__lesson', 'assignment__lesson__course'
    ).order_by('-submitted_at')
    
    # Фильтрация
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'pending':
        submissions = submissions.filter(grade__isnull=True)
    elif status_filter == 'graded':
        submissions = submissions.filter(grade__isnull=False)
    
    context = {
        'submissions': submissions,
        'status_filter': status_filter,
        'pending_count': Submission.objects.filter(grade__isnull=True).count(),
        'graded_count': Submission.objects.filter(grade__isnull=False).count(),
        'total_count': Submission.objects.count(),
    }
    return render(request, 'teacher/submissions.html', context)

@login_required
@teacher_required
def grade_submission(request, submission_id):
    """Страница оценки работы"""
    submission = get_object_or_404(Submission, id=submission_id)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        feedback = request.POST.get('feedback', '')
        
        if score:
            # Удаляем старую оценку если есть
            Grade.objects.filter(submission=submission).delete()
            
            # Создаем новую оценку
            Grade.objects.create(
                submission=submission,
                teacher=request.user,
                score=int(score),
                feedback=feedback
            )
            
            messages.success(request, f'Работа оценена на {score} баллов!')
            return redirect('teacher_submissions')
        else:
            messages.error(request, 'Пожалуйста, укажите оценку')
    
    # Получаем существующую оценку если есть
    existing_grade = Grade.objects.filter(submission=submission).first()
    
    context = {
        'submission': submission,
        'existing_grade': existing_grade,
        'max_score': submission.assignment.max_score,
    }
    return render(request, 'teacher/grade_submissions.html', context)

@login_required
@teacher_required
def teacher_admin(request):
    """Упрощенная админка для преподавателей"""
    context = {
        'courses_count': Course.objects.count(),
        'lessons_count': Lesson.objects.count(),
        'assignments_count': Assignment.objects.count(),
        'students_count': User.objects.filter(groups__name='Students').count(),
    }
    return render(request, 'teacher/admin.html', context)