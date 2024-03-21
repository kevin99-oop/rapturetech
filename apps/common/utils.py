from django.contrib.auth.decorators import user_passes_test

def staff_or_admin_required(user):
    return user.is_staff or user.is_superuser
