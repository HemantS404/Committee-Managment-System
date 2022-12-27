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
    path('Committee-registration/', CommitteeRegisterApi.as_view(), name = 'Committee-Registration'),
    path('Position-registration/', PositionRegisterApi.as_view(), name = 'Position-Registration'),
    path('Guide-registration/', GuideRegisterApi.as_view(), name = 'Guide-Registration'),
    path('Core-registration/', CoreRegisterApi.as_view(), name = 'Core-Registration'),
    path('CoCom-registration/', CoComRegisterApi.as_view(), name = 'CoCom-Registration'),
]