from django.contrib import admin
from users.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['role',]

admin.site.register(User, UserAdmin)
