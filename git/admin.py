from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from git.models import User, Repository


# ADMIN PAGE USER VIEW
class AccountAdmin(UserAdmin):
    list_display = ('username', 'token', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# ADMIN PAGE REPOSITORY VIEW
class RepositoryAdmin(ModelAdmin):
    list_display = ('user', 'owner', 'name', 'url')
    search_fields = ('user', 'owner', 'name')
    readonly_fields = ('user', 'owner', 'name', 'url')


admin.site.register(User, AccountAdmin)
admin.site.register(Repository, RepositoryAdmin)
