"""archt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# used for handle static files
from django.conf import settings

from django.contrib.auth import views as auth_views

# TODO: How to use another URLCONF such as "from blog import urls as
# blog_urls; url(r'^blog/', include(blog_urls)) ??????????"

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),

    # user-defined apps
    url(r'^simulator/', include('simulator.urls', namespace='simulator')),
    url(r'^performance/', include('performance.urls', namespace='performance')),
    url(r'^media/(?P<filename>.*)/$', 'publicView.download_filename'),

    # handle static files
    url(r'^static/(?P<path>.*)$','django.views.static.serve',
        {'document_root':settings.STATIC_ROOT}),

    #require login
    url(r'^accounts/login/$', auth_views.login),
]
