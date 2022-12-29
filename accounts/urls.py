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
    path('Committee/', CommitteeApi.as_view(), name = 'Committee'),
    path('Position/', PositionApi.as_view(), name = 'Position'),
    path('Guide/', GuideApi.as_view(), name = 'Guide'),
    path('Core/', CoreApi.as_view(), name = 'Core'),
    path('CoCom/', CoComApi.as_view(), name = 'CoCom'),
]