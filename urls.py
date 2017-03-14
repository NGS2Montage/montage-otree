from otree import urls
from django.contrib import admin
from django.conf.urls import url, include

from core import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^redirect/$', views.MyRedirectView.as_view(), name='redirect'),
    url(r'^oops/$', TemplateView.as_view(template_name='oops.html'), name='oops'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.MyRedirectView.as_view(), name='redirect'),
    url(r'^additional_user_info/$', TemplateView.as_view(template_name='additional_user_info.html'), name='additional-user-info'),
    url(r'', include(urls))
]
