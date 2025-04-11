from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView

from django.conf import settings
from django.contrib import messages

# ajax
from django.http import JsonResponse

# extra python imports
import webbrowser
import os

from .models import Board, Column, Card, Comment

from .forms import TrelloAddForm


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

# open transfer folders
@user_passes_test(lambda u: u.is_superuser)
def openTransferFolder(request):
    path=f"{settings.BASE_DIR}/temp/transfers"
    webbrowser.get("wslview %s").open(os.path.realpath(path))

def transferCheck(request):
    card_list = []
    cards = Card.objects.all()
    print(cards)
    # for card in cards:
    #     card_list.append[card.title, card.column, card.due_date]

    # transfer_dir = f"{settings.BASE_DIR}/PnaIT/temp/transfers"
    # folders = os.listdir(transfer_dir)
    # user_trello = TrelloKeys.objects.get(pk=request.user.id)
    # key = user_trello.trello_key
    # token = user_trello.trello_token
    # card_list = []

    # for board in board_names:
    #     ##get main data from trello Activities log
    #     trellodata = requests.get("https://api.trello.com/1/boards/"+board+"/actions/?limit=1000&key="+key+"&token="+token)
    #     print('trellodata: ', board, trellodata, trellodata.text)
    #     trellodata = trellodata.json()

    #     ####loop through data and find cards marked as done in the past 4 days
    #     for x in range(len(trellodata)):
    #     ##    if card is updated still active eg not achived
    #         if trellodata[x]["type"] == 'updateCard' and "closed" not in trellodata[x]["data"]["card"]:
    #     ##        card can be found in two places depending on the mood of Trello
    #     ##        this find the correct path
    #             try:
    #                 trellodata[x]["data"]["list"]["name"]
    #                 y = 'list'
    #             except:
    #                 trellodata[x]["data"]["listAfter"]["name"]
    #                 y = 'listAfter'
    #     ##        if card is marked as 'done'
    #             if trellodata[x]["data"][y]["name"] == 'Done':
    #                 if datetime.datetime.strptime(trellodata[x]["date"][:10], "%Y-%m-%d").date() >= datetime.date.today()-datetime.timedelta(4):
    #     ##                check if card is a folder in directory
    #                     if trellodata[x]["data"]["card"]["name"] in folders:
    #     ##                    add to card_list
    #                         if [trellodata[x]["date"][:10],
    #                         trellodata[x]["data"]["card"]["name"],
    #                         trellodata[x]["memberCreator"]["id"]] not in card_list:
    #                             card_list.append([trellodata[x]["date"][:10],
    #                             trellodata[x]["data"]["card"]["name"],
    #                             trellodata[x]["memberCreator"]["id"]])
    # print(card_list)
    # for card in card_list:
    #     if Branches.objects.filter(trello_id = card[2]).exists():
    #         card[2] = Branches.objects.get(trello_id = card[2]).branch_name

    # card_list.sort(reverse=True)
    # data = {
    # 'cards':card_list
    # }
    data = cards
    return JsonResponse(data)

def index(request):

    if 'trelloadd' in request.POST:
        form = TrelloAddForm(request.POST, prefix='trelloadd')
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            name = form.cleaned_data['name'].replace(",", "")
            due_date = form.cleaned_data['due_date']
            # user_trello = TrelloKeys.objects.get(pk=request.user.id)
            # key = user_trello.trello_key
            # token = user_trello.trello_token
            for branch in form.cleaned_data['branches']:
                print(branch.title)
                print(branch)
                Card.objects.create(
                    column = branch,
                    title = name,
                    due_date = due_date
                )
                # trello_id = branch.trello_id
                # params = {
                # "name":name,
                # "due":due_date,
                # # "idList":trello_lists["To Do"],
                # "idList":boards[branch.trello_board]["To do"],
                # "idMembers":trello_id,
                # "keepFromSource":"all",
                # "key":key,
                # "token":token
                # }
                # print(params)
                # response = requests.request("POST", "https://api.trello.com/1/cards", params=params)
                # print('response: ', response, response.text)
            messages.success(request, 'Saved Sucessfully')
        else:
            messages.error(request, form.errors)

    form = TrelloAddForm(prefix='trelloadd')

    # return render(request, './templates/admin_page.html', context=context)
    context = {
        'form':form,
        'cards' : Card.objects.all()
    }
    
    return render(request, 'boards/admin_page.html', context=context)

def getTransferData(request):
    branch = request.POST.get('branch')
    print(branch)
    # branch_id = Branches.objects.get(branch_name=branch).branch_id
    branch_id = branch
    transfer = request.POST.get('name')
    print(branch_id, transfer)
    file = open(f"{settings.BASE_DIR}/temp/transfers/"+transfer+"/"+branch_id+".txt")
    filedata = file.read()
    data = {
    'filedata': filedata,
    'transfer':transfer
    }
    print(data)
    return JsonResponse(data)