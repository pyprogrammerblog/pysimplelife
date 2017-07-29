from django.conf.urls import url
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    url(r'^home/$', views.Page1TemplateView.as_view(), name='index'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^app2/$', views.Page2TemplateView.as_view(), name='app2'),
    url(r'^app3/$', views.Page3TemplateView.as_view(), name='app3'),
    url(r'^app4/$', views.Page4TemplateView.as_view(), name='app4'),
    url(r'^app5/$', views.Page5TemplateView.as_view(), name='app5'),
    url(r'^app6/$', views.Page6TemplateView.as_view(), name='app6'),
    url(r'^app7/$', views.Page7TemplateView.as_view(), name='app7'),
]
