from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # frontpage
    url(r'^$', 'notes.views.frontpage'),

    # register
    url(r'^accounts/register/$', 'notes.views.register_user'),
    
    # auth
    url(r'^accounts/login/$', 'notes.views.login'),
    url(r'^accounts/logout/$', 'notes.views.logout'),
    url(r'^accounts/auth/$', 'notes.views.auth_view'),
    url(r'^accounts/invalid/$', 'notes.views.invalid_login'),
    
    # notes themselves
    url(r'^note/', include('usernotes.urls')),
    
    # admin
    url(r'^admin/', include(admin.site.urls)),    
)
