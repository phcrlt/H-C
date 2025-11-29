from django.contrib.auth.models import Group

def ensure_groups_exist():
    """
    Утилита для проверки существования необходимых групп
    """
    groups_created = []
    
    teachers_group, created = Group.objects.get_or_create(name='Teachers')
    if created:
        groups_created.append('Teachers')
    
    students_group, created = Group.objects.get_or_create(name='Students')
    if created:
        groups_created.append('Students')
    
    return groups_created

def get_user_role(user):
    """
    Возвращает роль пользователя
    """
    if user.groups.filter(name='Teachers').exists():
        return 'teacher'
    elif user.groups.filter(name='Students').exists():
        return 'student'
    else:
        return 'unknown'