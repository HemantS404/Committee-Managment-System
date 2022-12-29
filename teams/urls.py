from django.urls import path
from .views import *

urlpatterns = [
    path('Dashboard/', DashBoardApi.as_view(), name = 'dashboard'),
    path('Tasks/', TaskAssignApi.as_view(), name = 'Task'),
    path('Teams/', TeamApi.as_view(), name = 'Teams'),
]