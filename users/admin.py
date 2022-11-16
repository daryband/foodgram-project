from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class UserAdmin(BaseUserAdmin):
    list_filter = ('email', 'username')


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
