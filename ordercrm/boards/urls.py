from django.urls import path

from .views import BoardListView
from .views import BoardDetailView
from .views import CardDetailView
from .views import openTransferFolder
from .views import index
from .views import transferCheck
from .views import getTransferData


urlpatterns = [
    path('', BoardListView.as_view(), name='board_list'),
    path('<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('<int:board_id>/card/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('ajax/openTransferFolder', openTransferFolder, name='opentransferfolder'),
    path('admin_page', index),
    path('ajax/transfercheck', transferCheck, name='transfercheckajax'),
    path('ajax/getTransferData', getTransferData, name='getTransferData'),
]