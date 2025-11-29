from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, verbose_name='О себе')
    
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
    
    def __str__(self):
        return f'Профиль {self.user.username}'

# Сигнал для автоматического создания профиля при создании пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    instance.userprofile.save()
    
@receiver(post_save, sender=User)
def handle_user_save(sender, instance, created, **kwargs):
    """
    Обрабатывает создание и сохранение пользователя
    """
    if created:
        # Создаем профиль для нового пользователя
        UserProfile.objects.get_or_create(user=instance)
        
        # Автоматически добавляем в группу Students (если не админ)
        if not instance.is_superuser:
            try:
                students_group = Group.objects.get(name='Students')
                instance.groups.add(students_group)
            except Group.DoesNotExist:
                # Если группы нет - пропускаем, она будет создана через админку
                pass
    else:
        # При обновлении пользователя сохраняем профиль
        try:
            instance.userprofile.save()
        except UserProfile.DoesNotExist:
            UserProfile.objects.create(user=instance)