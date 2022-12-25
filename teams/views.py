from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import *
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DashBoardApi(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        mentor_team_data=[];mentee_team_data=[];task_given_data =[];task_have_data = []
        core_obj = Core.objects.filter(user = request.user)
        core_data = CoreSerializers(core_obj, many=True).data
        
        cocom_obj = CoCom.objects.filter(user = request.user)
        cocom_data = CoComSerializers(cocom_obj, many=True).data
        
        for i in core_obj:
            mentor_team_obj = Team.objects.filter(Mentors = i)
            mentor_team_data += TeamSerializer(mentor_team_obj, many=True).data
        
        for i in cocom_obj:
            mentee_team_obj = Team.objects.filter(Mentee = i)
            mentee_team_data += TeamSerializer(mentee_team_obj, many=True).data
        
        for i in core_obj:
            task_given_obj = Task.objects.filter(assigned_by =i)
            task_given_data += TaskSerializer(task_given_obj, many=True).data
        
        for i in cocom_obj:
            task_have_obj = AssignedTo.objects.filter(assgined_to =i)
            task_have_data += AssignedToSerializer(task_have_obj, many=True).data
        
        return Response({'User': str(request.user),'CoCom': cocom_data, 'Core': core_data,'Teams(as Mentor)': mentor_team_data,'Teams(as Mentee)' :mentee_team_data,'task_given' : task_given_data ,'task_have': task_have_data})

class TaskAssignApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

        serializer.save()

        mentees =  serializer.data['team_assign']['Mentee']
        for mentee in mentees:
            data_ = AssignedToSerializer(data = {'task':serializer.data['id'],'assgined_to':mentee})
            if not data_.is_valid():
                return Response({'status':403, 'errors': data_.errors, 'message': 'Some error has occured'})
            data_.save()
        return Response({'status': 200, 'message' : 'Task Assigned Sucessfully'})