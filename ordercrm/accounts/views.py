from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    return HttpResponse("Home", status=200)

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import RegisterForm


class RegisterView(SuccessMessageMixin, CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')
    form_class = RegisterForm
    success_message = "Your account was created successfully"