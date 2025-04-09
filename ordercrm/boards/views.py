from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from .models import Board, Column, Card, Comment


@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch', )
class BoardListView(ListView):
    template_name = "boards/board_list.html"

    def post(self, request, *args, **kwargs):  # <--
        title = request.POST.get("title")
        if title:
            Board.objects.create(title=title, owner=self.request.user)
        return redirect("boards")

    def get_queryset(self):
        return Board.get_available(self.request.user)

    def get_favorites_queryset(self):
        return Board.get_favorites(self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["favorite_object_list"] = self.get_favorites_queryset()
        return context

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch', )
class BoardDetailView(DetailView):
    template_name = "boards/board_detail.html"
    model = Board

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.get("action") == "create_column":
            title = request.POST.get("title")
            if title:
                Column.objects.create(
                    board=self.object,
                    title=title
                )
        if request.POST.get("action") == "create_card":
            title = request.POST.get("title")
            column = get_object_or_404(Column, pk=int(request.POST.get("column_id")))
            if title:
                Card.objects.create(title=title, column=column)

        if request.POST.get("action") == "move_card":   # Handle Drag and Drop
             if request.POST.get("column_id", None) is not None:
                 task = get_object_or_404(Card, pk=int(request.POST.get("task_id")))
                 column = get_object_or_404(Column, pk=int(request.POST.get("column_id")))
                 task.column = column
                 task.save()

        return redirect("board_detail", pk=self.object.pk)

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch', )
class CardDetailView(DetailView):
    template_name = "boards/card_detail.html"
    model = Card

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.POST.get("action") == "create_comment":
            text = request.POST.get("text")
            if text:
                Comment.objects.create(
                    author=self.request.user,
                    card=self.object,
                    text=text
                )
            return redirect("card_detail", pk=self.object.pk, board_id=self.object.column.board.pk)

        if request.POST.get("action") == "update_task":
            for field_name in ("title", "description"):
                if request.POST.get(field_name, None) is not None:
                    setattr(self.object, field_name, request.POST[field_name])

            if request.POST.get("column_id", None) is not None:
                column = get_object_or_404(Column, pk=int(request.POST.get("column_id")))
                self.object.column = column

            self.object.save()

            return HttpResponse("ok", status=200)
        return redirect("card_detail", pk=self.object.pk, board_id=self.object.column.board.pk)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = self.object.column.board
        return context