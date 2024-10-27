from django.contrib import admin

from .models import Questions, Users

admin.site.register(Questions)
admin.site.register(Users)