
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.contrib.auth import logout
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('wallet/', include('wallet.urls')),
    path('transactions/', include('transactions.urls')),
    path('signup/', include('users.urls')),
    path('api/', include('transactions.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]