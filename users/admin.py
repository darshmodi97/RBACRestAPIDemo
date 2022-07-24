from django.contrib import admin
from users.models import User, BlackListedToken
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'role']
    search_fields = ['email', 'first_name', 'last_name']
    list_filter = ['role',]


class BlackListedTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "timestamp", "jti_token")

admin.site.register(User, UserAdmin)
admin.site.register(BlackListedToken, BlackListedTokenAdmin)
