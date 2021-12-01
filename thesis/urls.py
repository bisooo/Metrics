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
from metrics.views.watchlist import watchlist
from metrics.views.typography import typography
from metrics.visuals import example

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dash/', dashboard, name='dashboard'),
    path('icons/', icons, name='icons'),
    path('notifications/', notifications, name='notifications'),
    path('profile/', profile, name='profile'),
    path('watchlist/', watchlist, name='watchlist'),
    path('typography/', typography, name='typo'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('admin/', admin.site.urls),
]
