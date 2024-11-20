from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
]   
