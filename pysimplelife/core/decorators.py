import datetime
from functools import wraps

from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import User


def confirm_password(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        last_login = request.user.last_login
        time_span = last_login + datetime.timedelta(hours=8)
        if timezone.now() > time_span:
            from .views import ConfirmationPasswordView
            return ConfirmationPasswordView.as_view()(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def delete_email_code(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email_verified and request.user.email_verification_code:
            user = get_object_or_404(User, pk=request.user.id)
            user.email_verification_code = None
            user.save()
        return view_func(request, *args, **kwargs)
    return _wrapped_view
