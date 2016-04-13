from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from usernotes.models import Usernote

urlpatterns = patterns('',
    url(r'^$', 'usernotes.views.notes_list'),    
    url(r'^(?P<note_id>\d+)/$', 'usernotes.views.note_view'),    
    url(r'^add/$', 'usernotes.views.add_note'),    
    url(r'^edit/(?P<note_id>\d+)/$', 'usernotes.views.edit_note'),
    
    
)
