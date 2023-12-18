from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('middle_name', 'phone_number', 'birth_date',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'middle_name', 'phone_number', 'is_staff', ]


admin.site.register(CustomUser, CustomUserAdmin)
