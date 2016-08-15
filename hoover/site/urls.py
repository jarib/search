from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from ..search.admin import admin_site
from ..search import views, uploads
from ..contrib.twofactor.views import AuthenticationForm
from ..contrib import installed

urlpatterns = [
    url(r'^_ping$', views.ping, name='ping'),
    url(r'^admin/', include(admin_site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^search$', views.search, name='search'),
    url(r'^whoami$', views.whoami, name='whoami'),
    url(r'^collections$', views.collections, name='collections'),
    url(r'^(?s)doc/(?P<collection_name>[^/]+)/(?P<id>.+)$', views.doc),
]

if installed.twofactor:
    from hoover.contrib.twofactor import views as twofactor_views
    from django.contrib.auth import views as auth_views
    urlpatterns += [
        url(r'^invitation/(?P<code>.*)$', twofactor_views.invitation),
        url(r'^accounts/login/$', auth_views.login, kwargs={
            'authentication_form': AuthenticationForm}),
    ]

urlpatterns += [
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^uploads/(?P<filename>.+)$', uploads.serve_file),
]
