from django.contrib import admin
from django.urls import path, include
# GIT
from git.views import register, login, logout
# METRICS
from metrics.views.homepage import homepage
from metrics.views.dashboard import dashboard
from metrics.views.profile import profile
from metrics.views.icons import icons
from metrics.views.notifications import notifications
from metrics.views.watchlist import watchlist, delete_repo
from metrics.views.watch_repo import watch_repo
from metrics.views.typography import typography
from metrics.visuals import example

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dash/', dashboard, name='dashboard'),

    path('icons/', icons, name='icons'),
    path('notifications/', notifications, name='notifications'),
    path('typography/', typography, name='typo'),

    path('watch/', watch_repo, name='watch_repo'),
    path('watchlist/', watchlist, name='watchlist'),
    path('watchlist/<int:repo_id>', delete_repo, name='delete_repo'),

    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('admin/', admin.site.urls),
]
