from django.utils.deprecation import MiddlewareMixin
from .utils import ensure_groups_exist

class EnsureGroupsMiddleware(MiddlewareMixin):
    """
    Middleware для проверки существования необходимых групп при запуске
    """
    def __init__(self, get_response):
        super().__init__(get_response)
        # Проверяем группы при инициализации middleware
        groups_created = ensure_groups_exist()
        if groups_created:
            print(f"✅ Созданы группы: {', '.join(groups_created)}")