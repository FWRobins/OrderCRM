from django.urls import path

from .views import BoardListView

urlpatterns = [
    path('', BoardListView.as_view(), name='board_list'),
]