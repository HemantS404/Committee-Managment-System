from django.urls import path
from .views import *

urlpatterns = [
    path('Dashboard/', DashBoardApi.as_view(), name = 'dashboard'),
    path('Tasks/', TaskAssignApi.as_view(), name = 'Task'),
    path('Tasks/<id>/', TaskAssignApi.as_view(), name = 'Task-Update-Delete'),
    path('Tasks/Assigned/<id>/', AssignedToApi.as_view(), name = 'Assigned-Task-Update'),
    path('Teams/', TeamApi.as_view(), name = 'Teams'),
    path('Teams/<id>/', TeamApi.as_view(), name = 'Teams-Update-Delete'),
    path('Teams/<operation>/<id>/', TeamUpdateApi.as_view(), name = 'Teams-Member-Update'),
]