from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from git.models import User


# ADMIN PAGE USER VIEW
class AccountAdmin(UserAdmin):
    list_display = ('username', 'token', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(User, AccountAdmin)
