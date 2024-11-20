from django.urls import path
from .views import signup_view
from . import views
from .api_views import RegisterUserView


urlpatterns = [
    path('', views.signup_view, name='signup'),
    # path('api/register/', RegisterUserView.as_view(), name='register_user'),
]
