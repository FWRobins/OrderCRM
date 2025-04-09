"""
URL configuration for ordercrm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

# from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import admin
from django.urls import path, include

from accounts import urls as accounts_urls
from boards import urls as boards_urls

# from accounts.views import dashboard

urlpatterns = [
    # path('accounts/login/', LoginView.as_view(
    #     template_name='accounts/login.html',
    #     redirect_authenticated_user=True,
    #     next_page='home'
    # ), name='login'),
    # path('accounts/logout/', LogoutView.as_view(
    #     template_name='accounts/logout.html',
    #     next_page = 'login',
    # ), name = 'logout'),
    # path('', dashboard, name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include(accounts_urls,)),
    path('boards/', include(boards_urls)),
]
