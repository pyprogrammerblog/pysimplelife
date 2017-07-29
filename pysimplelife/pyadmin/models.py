from django.db import models
from django.utils import timezone


# Create your models here.
class Manager(models.Model):
    """
    This model defines a manager. If a User has a Manager record, the User is a manager and ``user.is_manager`` will
    return ``True``.
    """

    manager = models.OneToOneField('core.User', on_delete=models.PROTECT)
    experience = models.CharField('Experience', default='no', max_length=100)
    position = models.CharField('Position', default='no', max_length=100)
    department = models.CharField('Department', default='no', max_length=100)

    def __str__(self):
        return 'Manager {}'.format(self.manager.get_full_name())

    class Meta:
        default_permissions = ['manage']
        ordering = ('manager__first_name',)


class Resource(models.Model):
    """
    This model defines a manager. If a User has a Manager record, the User is a manager and ``user.is_manager`` will
    return ``True``.
    """

    resource = models.OneToOneField('core.User', on_delete=models.PROTECT)
    experience = models.CharField('Experience', default='no', max_length=100)
    position = models.CharField('Position', default='no', max_length=100)
    department = models.CharField('Department', default='no', max_length=100)

    def __str__(self):
        return 'Resource {}'.format(self.resource.get_full_name())

    class Meta:
        default_permissions = ['manage']
        ordering = ('resource__first_name',)


class Project(models.Model):
    """
    This model defines a Project.
    """

    PHASE_CHOICES = (
        ('STG1', 'Stage1'),
        ('STG2', 'Stage2'),
        ('STG3', 'Stage3'),
        ('STG4', 'Stage4'),
        ('STG5', 'Stage5'),
    )

    name = models.CharField('Project Name', max_length=100)
    slug = models.SlugField('Project slug', unique=True)
    description = models.TextField('Description')

    start_date = models.DateTimeField(blank=False, null=False, default=timezone.now)
    due_date = models.DateTimeField(blank=False, null=False, default=timezone.now)
    date_completed = models.DateTimeField('Project completed', default=timezone.now)
    status = models.CharField(choices=PHASE_CHOICES, default='STG1', max_length=10)
    manager = models.ManyToManyField(Manager, through='ProjectManagerMembership')
    resource = models.ManyToManyField(Resource, through='ProjectResourceMembership')

    created_by = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='Created')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='Updated')
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return 'Project {}'.format(self.name)


class Task(models.Model):
    """
    This model defines a Group.
    """

    PRIORITY_CHOICES = (
        ('PRT1', 'Priority1'),
        ('PRT2', 'Priority2'),
        ('PRT3', 'Priority3'),
        ('PRT4', 'Priority4'),
    )

    name = models.CharField(max_length=100)
    slug = models.SlugField('Task slug', unique=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, default='PRT1', max_length=10)
    manager = models.ManyToManyField(Manager, through='TaskManagerMembership')
    resource = models.ManyToManyField(Resource, through='TaskResourceMembership')
    project = models.ForeignKey(Project)
    start_date = models.DateTimeField(blank=False, null=False, default=timezone.now)
    due_date = models.DateTimeField(blank=False, null=False, default=timezone.now)
    date_completed = models.DateTimeField('Project completed', default=timezone.now)

    created_by = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='Task_created')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(Manager, on_delete=models.PROTECT, related_name='Task_updated')
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return 'Task {}'.format(self.name)


class ProjectManagerMembership(models.Model):
    project = models.ForeignKey(Project)
    manager = models.ForeignKey(Manager, related_name='project_managed_by')
    date_joined = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64)
    feedback = models.CharField(max_length=64)
    assigned_by = models.ForeignKey('core.User', default=1, on_delete=models.PROTECT, related_name='manager_assigned_to_project')

    class Meta:
        ordering = ('project',)

    def __str__(self):
        return 'Project {}'.format(self.project.name)


class ProjectResourceMembership(models.Model):
    project = models.ForeignKey(Project)
    resource = models.ForeignKey(Resource, related_name='project_performed_by')
    date_joined = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64)
    feedback = models.CharField(max_length=64)
    assigned_by = models.ForeignKey(Manager, default=1, on_delete=models.PROTECT, related_name='resource_assigned_to_project')

    class Meta:
        ordering = ('project',)

    def __str__(self):
        return 'Project {}'.format(self.project.name)


class TaskManagerMembership(models.Model):
    task = models.ForeignKey(Task)
    manager = models.ForeignKey(Manager, related_name='task_managed_by')
    date_joined = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64)
    feedback = models.CharField(max_length=64)
    assigned_by = models.ForeignKey('core.User', default=1, on_delete=models.PROTECT, related_name='manager_assigned_to_task')

    class Meta:
        ordering = ('task',)

    def __str__(self):
        return '{}'.format(self.manager)


class TaskResourceMembership(models.Model):
    task = models.ForeignKey(Task)
    resource = models.ForeignKey(Resource, related_name='task_performed_by')
    date_joined = models.DateField(auto_now_add=True)
    invite_reason = models.CharField(max_length=64)
    feedback = models.CharField(max_length=64)
    assigned_by = models.ForeignKey(Manager, default=1, on_delete=models.PROTECT, related_name='resource_assigned_to_task')

    class Meta:
        ordering = ('task',)

    def __str__(self):
        return '{0}'.format(self.resource)
