# -*- coding: utf-8 -*-

from sys import exit
from django import forms
from django.utils.html import escape
# from django.http import HttpRequest
from usernotes.models import Usernote, Category

class UsernoteForm(forms.Form):
    title = forms.CharField(
        label = 'Заголовок', 
        max_length = 255, 
        required = True,
    )
    body = forms.CharField(
        label = 'Текст', 
        widget = forms.Textarea, 
        max_length = 50000,
        required = True,
    )    
    is_favorite = forms.BooleanField(
        label = 'Избранная',
        required = False,
    ) 
    status = forms.BooleanField(
        label = 'Опубликовать',
        initial = True,
        required = False,
    )
    category_id = forms.ChoiceField(
        label = 'Категория'
    )
    
    def __init__(self, *args, **kwargs):
        if 'usernote' in kwargs:
            self.usernote = kwargs['usernote']
        kwargs.pop('usernote', None)
        super(UsernoteForm, self).__init__(*args, **kwargs)
        categories = Category.objects.order_by('sort').values()[:30]
        choices = []
        for category in categories:
            choices.append([category['id'], category['title']])
        self.fields['category_id'].choices = choices
        
    def save(self, request = None):        
        if hasattr(self, 'usernote'): 
            usernote = self.usernote
        else:
            usernote = Usernote()
        
        data = self.cleaned_data        
        usernote.title = escape(data['title'])
        usernote.body = escape(data['body'])
        usernote.status = int(data['status'])
        usernote.is_favorite = int(data['is_favorite'])
        usernote.category_id = int(data['category_id'])
        
        if request:
            usernote.user_id = int(request.user.id)
        usernote.save()
