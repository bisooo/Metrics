from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin
from git.models import User, Repository, WatchList, PullRequestWait


# USER VIEW
class AccountAdmin(UserAdmin):
    list_display = ('username', 'token', 'date_joined', 'last_login', 'is_admin')
    search_fields = ('username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# REPOSITORY VIEW
class RepositoryAdmin(ModelAdmin):
    list_display = ('owner', 'name', 'url')
    search_fields = ('owner', 'name')
    readonly_fields = ('owner', 'name', 'url')


# WATCHLIST VIEW
class WatchListAdmin(ModelAdmin):
    list_display = ('user', 'repo')
    search_fields = ('user', 'repo')
    readonly_fields = ('user', 'repo')


# PULL REQUEST WAIT VIEW
class PRWaitAdmin(ModelAdmin):
    list_display = ('repo', 'number', 'created_at', 'merged_at', 'updated_at', 'merged')
    search_fields = ('repo', 'number', 'created_at', 'merged_at', 'updated_at', 'merged')
    readonly_fields = ('repo', 'number', 'created_at', 'merged_at', 'closed_at', 'updated_at', 'merged')


admin.site.register(User, AccountAdmin)
admin.site.register(Repository, RepositoryAdmin)
admin.site.register(WatchList, WatchListAdmin)
admin.site.register(PullRequestWait, PRWaitAdmin)

