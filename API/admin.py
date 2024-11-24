from django.contrib import admin

from .models import CustomUser, Questions, Answers, Favorites

class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'title','type')
    readonly_fields = ['id','user']
    fieldsets = (
        (None, {'fields': ('id','user', 'title','content', 'type')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'title','content' ,'type' ),
        }),
    )

admin.site.register(Questions,QuestionsAdmin)

class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id','question_id', 'is_true')
    readonly_fields = ['id','question_id']
    fieldsets = (
        (None, {'fields': ('id','question_id', 'is_true')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('question_id' ,'is_true' ),
        }),
    )
admin.site.register(Answers,AnswersAdmin)

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