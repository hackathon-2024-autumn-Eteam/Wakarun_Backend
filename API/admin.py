from django.contrib import admin

from .models import CustomUser, Questions, Answers, Favorites

admin.site.register(Questions)
admin.site.register(Answers)
admin.site.register(Favorites)

class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ('id','email', 'user_name') 
    readonly_fields = ['id']
    fieldsets = (
        (None, {'fields': ('id','email', 'user_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password', 'is_staff', 'is_active'),
        }),
    )
    ordering = ('email',)
    search_fields = ('email', 'user_name')

admin.site.register(CustomUser, CustomUserAdmin)