from django.urls import path
from .api_views import RegisterUserView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
]
