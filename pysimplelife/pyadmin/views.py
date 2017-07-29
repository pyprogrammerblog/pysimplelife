
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

from core.mixins import LoginRequiredMixin
from social_django.models import UserSocialAuth


# Create your views here.
class Page1TemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'pyadmin/index.html'


@login_required
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'pyadmin/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })


@method_decorator(login_required, name='dispatch')
class Page2TemplateView(TemplateView):
    template_name = 'pyadmin/bootstrap-elements.html'


@method_decorator(login_required, name='dispatch')
class Page3TemplateView(TemplateView):
    template_name = 'pyadmin/bootstrap-grid.html'


@method_decorator(login_required, name='dispatch')
class Page4TemplateView(TemplateView):
    template_name = 'pyadmin/charts.html'


@method_decorator(login_required, name='dispatch')
class Page5TemplateView(TemplateView):
    template_name = 'pyadmin/forms.html'


@method_decorator(login_required, name='dispatch')
class Page6TemplateView(TemplateView):
    template_name = 'pyadmin/index-rtl.html'


@method_decorator(login_required, name='dispatch')
class Page7TemplateView(TemplateView):
    template_name = 'pyadmin/tables.html'