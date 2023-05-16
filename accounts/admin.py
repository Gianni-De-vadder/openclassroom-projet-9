from django.contrib import admin
from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """Admin for the Review"""

    list_display = (
        "id",
        "username",
        "email",
        "last_login",
        "is_superuser",
        "password",
        "is_staff",
        "is_active",
        "date_joined",
    )


admin.site.register(User, UserAdmin)
