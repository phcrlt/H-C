from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Course(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    image = models.ImageField(upload_to='courses/', null=True, blank=True, verbose_name='Изображение')
    duration = models.CharField(max_length=50, verbose_name='Продолжительность')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner', verbose_name='Уровень')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    is_free = models.BooleanField(default=True, verbose_name='Бесплатный')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
    
    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200, verbose_name='Название')
    content = models.TextField(verbose_name='Содержание')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    duration = models.IntegerField(help_text='Длительность в минутах', verbose_name='Длительность')
    
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
class Assignment(models.Model):
    """Домашнее задание для урока"""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=200, verbose_name='Название задания')
    description = models.TextField(verbose_name='Описание задания')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True, verbose_name='Дедлайн')
    max_score = models.IntegerField(default=100, verbose_name='Максимальный балл')
    
    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

class Submission(models.Model):
    """Сдача задания студентом"""
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/%Y/%m/%d/', verbose_name='Файл работы')
    submitted_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True, verbose_name='Текст ответа')
    
    class Meta:
        verbose_name = 'Сдача работы'
        verbose_name_plural = 'Сдачи работ'
        ordering = ['-submitted_at']
        unique_together = ['assignment', 'student']
    
    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class Grade(models.Model):
    """Оценка за работу"""
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_grades')
    score = models.IntegerField(verbose_name='Баллы')
    feedback = models.TextField(blank=True, verbose_name='Комментарий преподавателя')
    graded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'
    
    def __str__(self):
        return f"{self.submission.student.username} - {self.score}"

class Comment(models.Model):
    """Комментарий к работе"""
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True)
    is_teacher_comment = models.BooleanField(default=False, verbose_name='Комментарий преподавателя')
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.author.username} - {self.text[:50]}"    