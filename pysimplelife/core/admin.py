from django.contrib import admin
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.admin import UserChangeForm, UserAdmin
from .models import User, GroupSettings


# Register your models here.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'email_verified', 'is_staff', 'groups', 'user_permissions',)


class CustomUserAdmin(UserAdmin):
    # Override standard fields
    form = CustomUserChangeForm
    fieldsets = None
    add_fieldsets = (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff',),
        }),

    list_display = ('is_active', 'email', 'last_login', 'email_verification_code',)
    list_display_links = ('email',)
    list_filter = ('is_active', 'last_login')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class GroupSettingsInline(admin.StackedInline):
    model = GroupSettings


class GroupAdmin(admin.ModelAdmin):
    model = Group
    inlines = [GroupSettingsInline]


admin.site.register(Permission)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
