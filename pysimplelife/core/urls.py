from django.conf.urls import url
from django.contrib.auth import views as django_auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'core'


urlpatterns = [
    url(r'^register/$', views.UserRegistrationView.as_view(), name='register'),
    url(r'^login/$', django_auth_views.LoginView.as_view(template_name='core/login.html',
           redirect_authenticated_user=True), name='login'),
    url(r'^logout/$', django_auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password_reset/$', django_auth_views.PasswordResetView.as_view(template_name='core/password_reset.html',
            email_template_name='core/password_reset_email.html', success_url=reverse_lazy('core:password_reset_done')),
            name='password_reset'),
    url(r'^password_reset_done/$', django_auth_views.PasswordResetDoneView.as_view(template_name='core/password_reset_done.html'),
            name='password_reset_done'),
    url(r'^password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            django_auth_views.PasswordResetConfirmView.as_view(template_name='core/password_reset_confirm.html',
            success_url=reverse_lazy('core:password_reset_complete')), name='password_reset_confirm'),
    url(r'^password_reset_complete/$', django_auth_views.PasswordResetCompleteView.as_view(template_name='core/password_reset_complete.html'),
            name='password_reset_complete'),
    url(r'^email_verification_required/$', views.EmailVerificationRequiredView.as_view(),
            name='email_verification_required'),
    url(r'^email_verify/(?P<user_id>\d+)/(?P<verification_code>[0-9A-Fa-f-]+)', views.EmailVerifyView.as_view(), name='email_verify'),
    # Dummy url to enable reversing without arguments
    url(r'^email_verify/', views.EmailVerifyView.as_view(), name='email_verify_dummy'),
    url(r'^login_redirect/$', views.LoginRedirectView.as_view(), name='login_redirect'),
    url(r'^password_change/$', django_auth_views.PasswordChangeView.as_view(template_name='core/password_change.html',
            success_url=reverse_lazy('core:password_change_done')),
            name='password_change'),
    url(r'^password_change_done/$', django_auth_views.PasswordChangeDoneView.as_view(template_name='core/password_change_done.html'),
            name='password_change_done'),
]
