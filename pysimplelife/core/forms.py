from django.contrib.auth.hashers import check_password
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from .models import User


class UserRegistrationForm(UserCreationForm):
    """
    This form is used to create a new user account.
    """

    email2 = forms.EmailField(required=True, label='Email confirmation')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'email2', 'password1', 'password2', ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit('submit', 'Register'))
        #self.fields['email2'].help_text = 'Enter your E-mail again to verify.'

    def clean(self):
        super(UserRegistrationForm, self).clean()

        if self.cleaned_data.get('email') and self.cleaned_data.get('email2'):
            if not self.cleaned_data.get('email') == self.cleaned_data.get('email2'):
                self._errors['email2'] = self.error_class(['There is a mismatch in your E-mail.'])

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save()
        user.send_email_verification_code()
        return user


class ConfirmationPasswordForm(forms.ModelForm):
    """
    This form is used to check if user is active.
    """

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['confirm_password', ]

    def clean(self):
        super(ConfirmationPasswordForm, self).clean()

        confirm_password = self.cleaned_data.get('confirm_password')
        if not check_password(confirm_password, self.instance.password):
            self.add_error('confirm_password', 'Password does not match.')

    def save(self, commit=True):
        user = super(ConfirmationPasswordForm, self).save()
        user.last_login = timezone.now()
        if commit:
            user.save()
        return user
