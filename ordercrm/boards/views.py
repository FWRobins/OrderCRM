from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .models import Board


@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch', )
class BoardListView(ListView):
    template_name = "boards/board_list.html"

    def get_queryset(self):
        return Board.get_available(self.request.user)

    def get_favorites_queryset(self):
        return Board.get_favorites(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["favorite_object_list"] = self.get_favorites_queryset()
        return context