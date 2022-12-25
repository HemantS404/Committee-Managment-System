from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('SignUp/', RegisterApi.as_view(), name = 'signup'),
    path('Logout/', LogoutApi.as_view(), name  = 'logout'),
    path('Login/', TokenObtainPairView.as_view(), name = 'login'),
    path('Login/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
]