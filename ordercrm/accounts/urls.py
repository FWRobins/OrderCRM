from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import  dashboard

urlpatterns = [
    path('login/', LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True,
        next_page="home",
    ), name='login'),
    path('logout/', LogoutView.as_view(
        next_page="login",
    ), name='logout'),
    path('', dashboard, name='home'),
]