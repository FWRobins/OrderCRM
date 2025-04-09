from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView


from accounts.views import  RegisterView, dashboard


urlpatterns = [
    path('login/', LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True,
        next_page="boards",
    ), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(
        next_page="login",
    ), name='logout'),
    path('', 
    RedirectView.as_view(
        url='boards'
    ), name='home'),
]