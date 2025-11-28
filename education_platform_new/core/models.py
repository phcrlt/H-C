from django.db import models
from django.contrib.auth.models import User

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