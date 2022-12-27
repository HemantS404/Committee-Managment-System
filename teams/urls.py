from django.urls import path
from .views import *

urlpatterns = [
    path('Dashboard/', DashBoardApi.as_view(), name = 'dashboard'),
    path('Task-Assign/', TaskAssignApi.as_view(), name = 'task-assign'),
    path('Team-Registration/', TeamRegisterApi.as_view(), name = 'Team-Registration'),
]