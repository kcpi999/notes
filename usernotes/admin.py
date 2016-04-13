from django.contrib import admin

# Register your models here.
from usernotes.models import Usernote
from usernotes.models import Category

admin.site.register(Usernote)
admin.site.register(Category)
