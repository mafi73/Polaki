from django.urls import path
from .views import WalletDashboardView


urlpatterns = [
     path('dashboard/', WalletDashboardView.as_view(), name='wallet_dashboard'),
]