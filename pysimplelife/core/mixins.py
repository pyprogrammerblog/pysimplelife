from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .decorators import confirm_password, delete_email_code


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    @method_decorator(confirm_password)
    @method_decorator(delete_email_code)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    @method_decorator(confirm_password)
    @method_decorator(delete_email_code)
    def dispatch(self, request, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(request, *args, **kwargs)
