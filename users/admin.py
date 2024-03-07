from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import LoginForm, ProfileForm
from users.models import User


class CustomUserAdmin(UserAdmin):
    """ Пользователь в административной панели. """

    add_form = LoginForm
    form = ProfileForm
    model = User

    list_display = ("id", "phone_number", "verify_code", "is_staff", "is_active",)
    list_filter = ("phone_number", "is_staff", "is_active",)

    # Поля "Основные" и "Права доступа" в административной панели
    # просмотра деталей пользователя.
    fieldsets = (
        ("Основные", {
            "fields": ("phone_number", "invite_code", "referred_by", "city", "avatar", "enter_code",)
        }
         ),
        ("Права доступа", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")
        }
         ),
    )
    # Поля для создания пользователя в административной панели.
    # "Wide" - класс для несворачиваемой панели с полями.
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone_number", "verify_code", "city", "avatar", "invite_code",
                "referred_by", "is_staff", "is_active", "groups", "user_permissions",
            )
        }
         ),
    )

    search_fields = ("phone_number",)
    ordering = ("phone_number",)


admin.site.register(User, CustomUserAdmin)
