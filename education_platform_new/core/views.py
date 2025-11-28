from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
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
    lessons = Lesson.objects.select_related('course').all()
    context = {
        'lessons': lessons
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