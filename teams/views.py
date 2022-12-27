from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
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
        try:
            team_mentors_id = TeamSerializer(Team.objects.get(id = request.data['team_assign'])).data['Mentors']
            user_core_positions = [x['id'] for x in CoreSerializers(Core.objects.filter(user = request.user), many = True).data]
            for core_id in user_core_positions:
                if core_id in team_mentors_id:
                    serializer = TaskSerializer(data = {'task_name':request.data['task_name'],'description' : request.data['description'],'team_assign' : request.data['team_assign'], 'assigned_by': core_id, 'material' : request.data['material']})
                    if not serializer.is_valid():
                        return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

                    serializer.save()

                    mentees =  serializer.data['team_assign']['Mentee']
                    for mentee in mentees:
                        data_ = AssignedToSerializer(data = {'task':serializer.data['id'],'assgined_to':mentee})
                        if not data_.is_valid():
                            return Response({'status':403, 'errors': data_.errors, 'message': 'Some error has occured'})
                        data_.save()
                    return Response({'status': 200, 'payload': {'Task_id' : serializer.data['id']},'message' : 'Task Assigned Sucessfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Team','message' : 'Bad Request'})
        except Exception as e:
            print(e)
            serializer = TaskSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

class TeamRegisterApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        
        try:
            if (int(request.data['belongs_to']) in core_committee_id):
                data = request.data
                
                mentor_list=data["Mentors"].strip('][}{)(').split(',')
                core_list = [x['id'] for x in Core.objects.filter(committee = data['belongs_to']).values()]
                for i in mentor_list:
                    if int(i) not in core_list:
                        return Response({'status': 403, 'error' : f"id : {i} is not in Committee's Core ",'message' : 'Bad Request'})

                mentee_list=data["Mentee"].strip('][}{)(').split(',')
                cocom_list = [x['id'] for x in CoCom.objects.filter(committee = data['belongs_to']).values()]
                for i in mentee_list:
                    if int(i) not in cocom_list:
                        return Response({'status': 403, 'error' : f"id : {i} is not in Committee's CoCom ",'message' : 'Bad Request'})

                serializer = TeamSerializer(data ={'team_name' : data["team_name"], 'belongs_to' : data['belongs_to'],'Mentors':mentor_list,'Mentee':mentee_list})
                if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                serializer.save()
                return Response({'status':200, 'payload': {'Team_id' : serializer.data['id']}, 'message': 'Team Registered Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except :
            serializer = TeamSerializer(data = request.data)
            if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})