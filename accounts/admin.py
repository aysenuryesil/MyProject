from django.contrib import admin
from django.contrib.auth.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active")

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

