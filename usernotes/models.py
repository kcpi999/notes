# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """
    Категория заметки
    """
    # название категории
    title = models.CharField(max_length = 50)
    # описание категории
    description = models.CharField(max_length = 255)
    # сортировка
    sort = models.IntegerField(max_length = 5)
    
    def __unicode__(self):
        return self.title

class Usernote(models.Model):
    """
    Заметка
    """
    # заголовок
    title = models.CharField(max_length = 255)
    # текст заметки
    body = models.TextField()
    # дата создания
    created = models.DateTimeField(auto_now_add = True)
    # категория
    #category_id = models.IntegerField(max_length = 10)
    category = models.ForeignKey(Category)
    # автор
    #user_id = models.IntegerField(max_length = 10)
    user = models.ForeignKey(User)
    # статус (Опубликована: 1, неопубликована: 0)
    status = models.IntegerField(max_length = 1)
    # избранная (1 / 0)
    is_favorite = models.IntegerField(max_length = 1)
    # uuid, длинный токен для прямой ссылки неавторизованным юзерам
    uuid = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title
