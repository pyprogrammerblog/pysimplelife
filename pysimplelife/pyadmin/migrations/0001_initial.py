# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 20:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(default='no', max_length=100, verbose_name='Experience')),
                ('position', models.CharField(default='no', max_length=100, verbose_name='Position')),
                ('department', models.CharField(default='no', max_length=100, verbose_name='Department')),
                ('manager', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': ['manage'],
                'ordering': ('manager__first_name',),
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Project Name')),
                ('slug', models.SlugField(unique=True, verbose_name='Project slug')),
                ('description', models.TextField(verbose_name='Description')),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_completed', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Project completed')),
                ('status', models.CharField(choices=[('STG1', 'Stage1'), ('STG2', 'Stage2'), ('STG3', 'Stage3'), ('STG4', 'Stage4'), ('STG5', 'Stage5')], default='STG1', max_length=10)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Created', to='pyadmin.Manager')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ProjectManagerMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('invite_reason', models.CharField(max_length=64)),
                ('feedback', models.CharField(max_length=64)),
                ('assigned_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='manager_assigned_to_project', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_managed_by', to='pyadmin.Manager')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyadmin.Project')),
            ],
            options={
                'ordering': ('project',),
            },
        ),
        migrations.CreateModel(
            name='ProjectResourceMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('invite_reason', models.CharField(max_length=64)),
                ('feedback', models.CharField(max_length=64)),
                ('assigned_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='resource_assigned_to_project', to='pyadmin.Manager')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyadmin.Project')),
            ],
            options={
                'ordering': ('project',),
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('experience', models.CharField(default='no', max_length=100, verbose_name='Experience')),
                ('position', models.CharField(default='no', max_length=100, verbose_name='Position')),
                ('department', models.CharField(default='no', max_length=100, verbose_name='Department')),
                ('resource', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'default_permissions': ['manage'],
                'ordering': ('resource__first_name',),
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(unique=True, verbose_name='Task slug')),
                ('priority', models.CharField(choices=[('PRT1', 'Priority1'), ('PRT2', 'Priority2'), ('PRT3', 'Priority3'), ('PRT4', 'Priority4')], default='PRT1', max_length=10)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('due_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_completed', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Project completed')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Task_created', to='pyadmin.Manager')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TaskManagerMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('invite_reason', models.CharField(max_length=64)),
                ('feedback', models.CharField(max_length=64)),
                ('assigned_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='manager_assigned_to_task', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_managed_by', to='pyadmin.Manager')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyadmin.Task')),
            ],
            options={
                'ordering': ('task',),
            },
        ),
        migrations.CreateModel(
            name='TaskResourceMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('invite_reason', models.CharField(max_length=64)),
                ('feedback', models.CharField(max_length=64)),
                ('assigned_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='resource_assigned_to_task', to='pyadmin.Manager')),
                ('resource', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_performed_by', to='pyadmin.Resource')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyadmin.Task')),
            ],
            options={
                'ordering': ('task',),
            },
        ),
        migrations.AddField(
            model_name='task',
            name='manager',
            field=models.ManyToManyField(through='pyadmin.TaskManagerMembership', to='pyadmin.Manager'),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pyadmin.Project'),
        ),
        migrations.AddField(
            model_name='task',
            name='resource',
            field=models.ManyToManyField(through='pyadmin.TaskResourceMembership', to='pyadmin.Resource'),
        ),
        migrations.AddField(
            model_name='task',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Task_updated', to='pyadmin.Manager'),
        ),
        migrations.AddField(
            model_name='projectresourcemembership',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_performed_by', to='pyadmin.Resource'),
        ),
        migrations.AddField(
            model_name='project',
            name='manager',
            field=models.ManyToManyField(through='pyadmin.ProjectManagerMembership', to='pyadmin.Manager'),
        ),
        migrations.AddField(
            model_name='project',
            name='resource',
            field=models.ManyToManyField(through='pyadmin.ProjectResourceMembership', to='pyadmin.Resource'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Updated', to='pyadmin.Manager'),
        ),
    ]
