from django.contrib import admin

from .models import User


class AdminUser(admin.ModelAdmin):
    list_display = ['username', 'bio', 'role']


admin.site.register(User, AdminUser)
