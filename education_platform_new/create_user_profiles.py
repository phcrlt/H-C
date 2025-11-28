from accounts.models import UserProfile
from django.contrib.auth.models import User
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'education_platform_new.settings')
django.setup()


def create_missing_profiles():
    users_without_profile = User.objects.filter(userprofile__isnull=True)
    count = 0

    for user in users_without_profile:
        UserProfile.objects.create(user=user)
        count += 1
        print(f'Created profile for user: {user.username}')

    print(f'Created {count} user profiles')


if __name__ == '__main__':
    create_missing_profiles()
