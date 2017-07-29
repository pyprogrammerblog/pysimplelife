import datetime

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import User


def EmailVerificationRequiredMiddleware(get_response):
    """
    This middleware redirects the user to a notice that their email address needs to be verified before they can
    continue if they are logged in and have passed SMS verification.
    """

    def middleware(request):
        if request.user.is_authenticated \
                and not reverse('core:email_verification_required') in request.path \
                and not reverse('core:email_verify_dummy') in request.path \
                and not reverse('core:logout') in request.path:
            if not request.user.email_verified:
                return redirect('core:email_verification_required')

        response = get_response(request)
        return response

    return middleware
