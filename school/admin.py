from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser, Teacher, Parent, Student, Class


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'gender', 'last_connexion', 'photo_preview')
    list_filter = ('role', 'gender')
    readonly_fields = ('last_connexion', 'photo_preview')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'photo')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'last_connexion')}),
        ('Additional info', {
            'fields': ('role', 'gender', 'address', 'phone'),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'gender', 'photo'),
        }),
    )

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.photo.url)
        return "(Aucune photo)"

    photo_preview.short_description = "Photo actuelle"

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'diploma', 'specialization', 'hiring_date')
    list_filter = ('diploma', 'hiring_date')

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'parent_type', 'spouse')
    list_filter = ('parent_type',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricule', 'class_level', 'parent')
    list_filter = ('class_level',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(CustomUser, CustomUserAdmin)