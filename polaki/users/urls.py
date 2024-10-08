from django.urls import path
from .views import signup_view
from . import views

urlpatterns = [
    path('', views.signup_view, name='signup'),
]
