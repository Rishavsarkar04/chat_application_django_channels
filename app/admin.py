from django.contrib import admin
from app.models import *
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.


class MyUserAdmin(UserAdmin):
  
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','username', 'mobile_number','is_online')
    list_display_links = ('username',)
    list_filter = ('is_admin',)
    fieldsets = (
        ('user credential', {'fields': ('username', 'email','password',)}),
        ('Personal info', {'fields': ('mobile_number','is_online')}),
        ('Permissions', {'fields': ('is_admin','is_active','is_staff','is_superuser','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('username','id')

# Now register the new UserAdmin...
admin.site.register(MyUser,MyUserAdmin)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver','group_name','message','is_seen')






