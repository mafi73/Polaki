from django.urls import path
from .views import add_transaction

urlpatterns = [
    path('add/', add_transaction, name='add_transaction'),
]
