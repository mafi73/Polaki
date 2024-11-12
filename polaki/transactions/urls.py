from django.urls import path
from .views import add_transaction
from . import views
from rest_framework.routers import DefaultRouter
# from .views import TransactionViewSet

# router = DefaultRouter
# router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('add/', add_transaction, name='add_transaction'),
    path('list/',views.transactions_list, name='transaction_list'),
    path('update/<int:transaction_id>/', views.update_transaction, name='update_transaction'),
    path('delete/<int:transaction_id>/', views.delet_transaction, name='delete_transaction'),
    # path('api/', include(router.urls)),
]   
