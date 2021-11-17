"""thesis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from metrics.views import homepage, dashboard, profile, icons, login, notifications, tables, typography
from metrics.visuals import example

urlpatterns = [
    path('', homepage, name='homepage'),
    path('dash/', dashboard, name='dashboard'),
    path('icons/', icons, name='icons'),
    path('notifications/', notifications, name='notifications'),
    path('profile/', profile, name='profile'),
    path('tables/', tables, name='tables'),
    path('typography/', typography, name='typo'),
    path('login/', login, name='login'),

    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('admin/', admin.site.urls),
]
