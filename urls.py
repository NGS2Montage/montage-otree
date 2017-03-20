from otree import urls
from django.contrib import admin
from django.conf.urls import url, include

from core import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', views.MyRedirectView.as_view(), name='redirect'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^redirect/$', views.MyRedirectView.as_view(), name='redirect'),
    url(r'^create_account/key/(?P<uid>[0-9A-Za-z]+)-(?P<key>.+)-(?P<sid>[0-9A-Za-z]+)/$', views.create_account,
        name='create_account_from_key'),
    url(r'^account_created/$', TemplateView.as_view(template_name='account/account_creation_done.html'),
        name='account_created'),
    url(r'^no_association/$', TemplateView.as_view(template_name='no_association.html'), name='no-association'),
    url(r'^no_consent/$', TemplateView.as_view(template_name='no_consent.html'), name='no-consent'),
    url(r'^max_participants/$', TemplateView.as_view(template_name='max_participants.html'), name='max-participants'),
    url(r'^oops/$', TemplateView.as_view(template_name='oops.html'), name='oops'),
    url(r'^additional_user_info/$', views.AdditionUserView.as_view(template_name='additional_user_info.html'),
        name='additional-user-info'),
    url(r'', include(urls))
]
