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
    path('Committee/<id>/', CommitteeApi.as_view(), name = 'Committee-Update-Delete'),
    path('Position/', PositionApi.as_view(), name = 'Position'),
    path('Position/<id>/', PositionApi.as_view(), name = 'Position-Update-Delete'),
    path('Guide/', GuideApi.as_view(), name = 'Guide'),
    path('Guide/<id>/', GuideApi.as_view(), name = 'Guide-Delete'),
    path('Core/', CoreApi.as_view(), name = 'Core'),
    path('Core/<id>/', CoreApi.as_view(), name = 'Core-Delete'),
    path('CoCom/', CoComApi.as_view(), name = 'CoCom'),
    path('CoCom/<id>/', CoComApi.as_view(), name = 'CoCom-Delete'),
    path('User-Update/', UserApi.as_view(), name='User-Update'),
]