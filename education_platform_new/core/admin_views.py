from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Course, Lesson, Assignment

@staff_member_required
def admin_dashboard(request):
    context = {
        'user_count': User.objects.count(),
        'course_count': Course.objects.count(),
        'lesson_count': Lesson.objects.count(),
        'assignment_count': Assignment.objects.count(),
    }
    return render(request, 'admin/index.html', context)