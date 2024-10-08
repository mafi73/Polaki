from django.urls import path
from .views import add_transaction
from . import views

urlpatterns = [
    path('add/', add_transaction, name='add_transaction'),
    path('list/',views.transactions_list, name='transaction_list')
]
