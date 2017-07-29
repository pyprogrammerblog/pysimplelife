from django.contrib import admin
from django import forms
from .models import Manager, Project, Task, Resource, ProjectManagerMembership, ProjectResourceMembership, \
    TaskManagerMembership, TaskResourceMembership


# Register your models here.
class TaskManagerMemberAdminForm(forms.ModelForm):
    class Meta:
        model = TaskManagerMembership
        fields = ['task', 'manager', 'invite_reason', 'feedback']

    def clean(self, ):
        if not self.cleaned_data.get('manager').id in ProjectManagerMembership.objects.filter(project__task=self.cleaned_data.get('task')).values_list('manager__id', flat=True):
            raise forms.ValidationError("You must select a manager available for this project!")
        if 'manager' in self.changed_data or 'task' in self.changed_data:
            if TaskManagerMembership.objects.filter(manager=self.cleaned_data.get('manager')).exists():
                raise forms.ValidationError("You got duplicated manager for this task!")
        return super(TaskManagerMemberAdminForm, self).clean()


class TaskManagerMemberAdmin(admin.ModelAdmin):

    form = TaskManagerMemberAdminForm
    list_display = ['__str__', 'task', 'invite_reason', 'date_joined', 'feedback',]
    list_filter = ['manager']


class TaskResourceMemberAdminForm(forms.ModelForm):
    class Meta:
        model = TaskResourceMembership
        fields = ['task', 'resource', 'invite_reason', 'feedback']

    def clean(self, ):
        if not self.cleaned_data.get('resource').id in ProjectResourceMembership.objects.filter(project__task=self.cleaned_data.get('task')).values_list('resource__id', flat=True):
            raise forms.ValidationError("You must select a resource available for this project!")
        if 'resource' in self.changed_data or 'task' in self.changed_data:
            if TaskResourceMembership.objects.filter(resource=self.cleaned_data.get('resource')).exists():
                raise forms.ValidationError("You got duplicated resource for this task!")
        return super(TaskResourceMemberAdminForm, self).clean()


class TaskResourceMemberAdmin(admin.ModelAdmin):

    form = TaskResourceMemberAdminForm

    list_display = ['__str__', 'task', 'invite_reason', 'date_joined', 'feedback',]
    list_filter = ['task']


class ProjectManagerMembershipAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectManagerMembership
        fields = ['project', 'manager', 'invite_reason', 'feedback']

    def clean(self, ):
        if ProjectManagerMembership.objects.filter(manager=self.cleaned_data.get('manager')).exists():
            raise forms.ValidationError("You got a duplicated manager for this project!")
        return super(ProjectManagerMembershipAdminForm, self).clean()


class ProjectManagerMembershipAdmin(admin.ModelAdmin):

    form = ProjectManagerMembershipAdminForm

    list_display = ['project', 'manager', 'invite_reason', 'date_joined', 'feedback',]
    list_filter = ['project']


class ProjectResourceMembershipAdminForm(forms.ModelForm):
    class Meta:
        model = ProjectResourceMembership
        fields = ['project', 'resource', 'invite_reason', 'feedback']

    def clean(self):
        if ProjectResourceMembership.objects.filter(resource=self.cleaned_data.get('resource')).exists():
            raise forms.ValidationError("You got a duplicated resource for this project!")
        return super(ProjectResourceMembershipAdminForm, self).clean()


class ProjectResourceMembershipAdmin(admin.ModelAdmin):

    form = ProjectResourceMembershipAdminForm

    list_display = ['project', 'resource', 'invite_reason', 'date_joined', 'feedback',]
    list_filter = ['resource']


class ManagerAdmin(admin.ModelAdmin):
    ordering = ['manager',]
    list_display = ['manager', 'experience', 'position', 'department']
    list_filter = ['manager']


class ResourceAdmin(admin.ModelAdmin):
    ordering = ['resource',]
    list_display = ['resource', 'experience', 'position', 'department']
    list_filter = ['resource']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'due_date', 'date_completed', 'status', 'created_by', 'updated_by']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'start_date', 'due_date', 'date_completed', 'created_by', 'updated_by']


admin.site.register(Manager, ManagerAdmin)
admin.site.register(Resource, ResourceAdmin)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)

admin.site.register(ProjectManagerMembership, ProjectManagerMembershipAdmin)
admin.site.register(ProjectResourceMembership, ProjectResourceMembershipAdmin)

admin.site.register(TaskManagerMembership, TaskManagerMemberAdmin)
admin.site.register(TaskResourceMembership, TaskResourceMemberAdmin)
