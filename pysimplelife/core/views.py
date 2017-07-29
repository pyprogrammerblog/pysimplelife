from django.views.generic import CreateView, TemplateView, View, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseNotFound

from .models import User
from .forms import UserRegistrationForm
from .forms import ConfirmationPasswordForm
from .mixins import LoginRequiredMixin



class UserRegistrationView(SuccessMessageMixin, CreateView):
    """
    This class is used for user registration
    """

    model = User
    form_class = UserRegistrationForm
    template_name = 'core/register.html'

    success_message = 'Your account has been created and you can now log in. Check your email for a message ' \
                      'about confirming your email address.'
    success_url = reverse_lazy('core:login')


class EmailVerifyView(View):
    """
    This class change verified true by clicking
    """

    def get(self, request, *args, **kwargs):
        if not self.kwargs.get('user_id') or not self.kwargs.get('verification_code'):
            return HttpResponseNotFound

        user = get_object_or_404(User, pk=self.kwargs['user_id'],
                                 email_verification_code=self.kwargs['verification_code'])
        user.email_verified = True
        # user.email_verification_code = None
        user.save()
        return render(request, 'core/email_verification.html')


class EmailVerificationRequiredView(LoginRequiredMixin, TemplateView):
    """
    EmailVerificationRequiredMiddleware redirects the user to this view as long as their email address is not verified.
    """

    template_name = 'core/email_verification_required.html'


class LoginRedirectView(LoginRequiredMixin, View):
    """
    This view determines where to send the user after logging in. If the user is a pharmacist or a manager they will
    be sent to those sections respectively. If the user is a patient but does not have any coupled patients, the user
    is redirected to coupling their first patient. If the user is a patient and has at least one coupled patient they
    will be sent to the patient section.
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return redirect(reverse_lazy('pyadmin:index'))
        elif request.user.is_authenticated:
            return redirect(reverse_lazy('pyadmin:index'))
        else:
            return redirect(reverse_lazy('public:index'))


class ConfirmationPasswordView(UpdateView):

    form_class = ConfirmationPasswordForm
    template_name = 'core/confirmation_password.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.get_full_path()
