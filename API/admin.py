from django.contrib import admin

from .models import Users, Questions, Answers, Favorites

admin.site.register(Users)
admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Favorites)