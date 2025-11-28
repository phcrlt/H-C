from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Course, Lesson, Assignment, Submission, Grade, Comment

def home(request):
    courses = Course.objects.all()[:6]
    context = {
        'courses': courses
    }
    return render(request, 'index.html', context)

def home_simple(request):
    return render(request, 'index_simple.html')

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
        
        # Создаем новую сдачу
        file = request.FILES.get('file')
        text = request.POST.get('text', '')
        
        if not file:
            messages.error(request, 'Пожалуйста, загрузите файл с работой')
            return redirect('assignment_detail', assignment_id=assignment_id)
        
        submission = Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=file,
            text=text
        )
        
        messages.success(request, 'Работа успешно сдана на проверку!')
        return redirect('assignment_detail', assignment_id=assignment_id)
    
    return redirect('assignment_detail', assignment_id=assignment_id)