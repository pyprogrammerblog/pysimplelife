import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group
from django.db import models
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings


class UserManager(BaseUserManager):
    """
    This model remake Django's built-in User model in order to login with email.
    """

    def create_user(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        if not email:
            raise ValueError('Enter an email address')
        if not first_name:
            raise ValueError('Enter a first name')
        if not last_name:
            raise ValueError('Enter a last name')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, first_name=None, last_name=None, **extra_fields):
        user = self.create_user(email=email, password=password, first_name=first_name, last_name=last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    # Verification fields
    email = models.EmailField('Email', unique=True, validators=[validate_email])
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('is active', default=True)
    is_staff = models.BooleanField('is staff', default=False)

    # Verification fields
    email_verified = models.BooleanField(default=False)
    email_verification_code = models.UUIDField(default=uuid.uuid4, null=True)

    # Other fields
    updated = models.DateTimeField('updated', auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        #return reverse('users:profile', args=[self.pk])
        return redirect('/')

    class Meta:
        default_permissions = ['manage']
        ordering = ('first_name',)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.get_full_name()

    def send_email_verification_code(self):
        """
        Sends the user an email with a link to click to verify their email address
        """

        if self.email_verification_code:
            verification_code = self.email_verification_code
        else:
            verification_code = uuid.uuid4()
            self.email_verification_code = verification_code
            self.save()

        context = {
            'link': 'http://127.0.0.1:8000' +
                    str(reverse_lazy('core:email_verify',
                                     kwargs={'user_id': self.id, 'verification_code': verification_code}))
        }
        subject = 'Welcome to PySimplelife.com'
        message = 'In order to finish registration please click in this email -> ' + str(context['link'])
        from_email = settings.EMAIL_HOST_USER
        to_list = [self.email, settings.EMAIL_HOST_USER]
        send_mail(subject, message, from_email, to_list, fail_silently=False)


class GroupSettings(models.Model):
    """
    This model extends Django's built-in Group model with more attributes.
    """

    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    default_manager_group = models.BooleanField(default=False)

    def __str__(self):
        return 'Group {} settings'.format(self.group.name)

    class Meta:
        default_permissions = ['manage']

