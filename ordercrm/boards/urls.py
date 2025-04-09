from django.urls import path

from .views import BoardListView, BoardDetailView, CardDetailView


urlpatterns = [
    path('', BoardListView.as_view(), name='board_list'),
    path('<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('<int:board_id>/card/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
]