from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from .serializers import *
from rest_framework.response import Response
from .models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.custompermission import IsVerified

# Create your views here.
class DashBoardApi(GenericAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def get(self, request):
        mentor_team_data=[];mentee_team_data=[];task_given_data =[];task_have_data = []
        core_obj = Core.objects.filter(user = request.user)
        core_data = [{"committee" : x["committee"]["Committee_name"], "position" : x["position"]["Position_name"]} for x in CoreSerializers(core_obj, many=True).data]
        
        cocom_obj = CoCom.objects.filter(user = request.user)
        cocom_data = [{"committee" : x["committee"]["Committee_name"], "position" : x["position"]["Position_name"]} for x in CoComSerializers(cocom_obj, many=True).data]
        
        for i in core_obj:
            mentor_team_obj = Team.objects.filter(Mentors = i)
            mentor_team_data+=([{
                'Team Name' : x["team_name"], 
                'Belongs To' : x["belongs_to"]["Committee_name"],   
                } for x in TeamSerializer(mentor_team_obj, many=True).data])
        
        for i in cocom_obj:
            mentee_team_obj = Team.objects.filter(Mentee = i)
            mentee_team_data+=([{
                'Team Name' : x["team_name"], 
                'Belongs To' : x["belongs_to"]["Committee_name"],  
                } for x in TeamSerializer(mentee_team_obj, many=True).data])
        
        for i in core_obj:
            task_given_obj = Task.objects.filter(assigned_by =i)
            task_given_data +=[{
                "Team Name" : x["team_assign"]["team_name"],
                "Task Name" : x["task_name"]
                } for x in TaskSerializer(task_given_obj, many=True).data]
        
        for i in cocom_obj:
            task_have_obj = AssignedTo.objects.filter(assgined_to =i)
            task_have_data += [{
                "Team Name" : x["task"]["team_assign"]["team_name"],
                "Task Name" : x["task"]["task_name"], 
                "Submitted" : x["submitted"], 
                "Assigned By": {
                    "First Name" : x["task"]["assigned_by"]["user"]["First_name"], 
                    "Last Name" : x["task"]["assigned_by"]["user"]["Last_name"]
                    }} for x in  AssignedToSerializer(task_have_obj, many=True).data]
        
        completed_task = [x for x in task_have_data if x["Submitted"] == True]
        incomplete_task = [x for x in task_have_data if x["Submitted"] == False]
        
        return Response({'User': str(request.user),'CoCom': cocom_data, 'Core': core_data,'Teams(as Mentor)': mentor_team_data,'Teams(as Mentee)' :mentee_team_data,'task_given' : task_given_data ,'Completed Task': completed_task, "Incomplete Task":incomplete_task})

class TaskAssignApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def delete(self, request, id = None):
        try:
            task_obj = Task.objects.get(id =id)
            team_Mentors = TaskSerializer(task_obj).data['team_assign']['Mentors']
            core_id = [x['id'] for x in Core.objects.filter(user = request.user).values()]
            for x in core_id:
                if x in team_Mentors:
                    task_obj.delete()
                    return Response({'status':200, 'payload': {'Task_id' : id}, 'message': 'Task Deleted Successfully'})
            else:        
                return Response({'status': 403, 'error' : 'Not a Mentor in the Entered Task\'s Team','message' : 'Bad Request'})
        except Exception as e:
            print(e)
            return Response({'status': 403, 'message' : 'Invalid Id'})

    def patch(self, request, id):
        try:
            task_obj = Task.objects.get(id =id)
            team_Mentors = TaskSerializer(task_obj).data['team_assign']['Mentors']
            core_id = [x['id'] for x in Core.objects.filter(user = request.user).values()]
            for x in core_id:
                if x in team_Mentors:
                    serializer = TaskSerializer(task_obj, data = request.data, partial =True)
                    if not serializer.is_valid():
                        return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                    serializer.save()
                    return Response({'status':200, 'payload': {'Task_id' : serializer.data['id']}, 'message': 'Task Updated Successfully'})
            else:        
                return Response({'status': 403, 'error' : 'Not a Mentor in the Entered Task\'s Team','message' : 'Bad Request'})
        except Exception as e:
            print(e)
            return Response({'status': 403, 'message' : 'Invalid Id'})

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
    
    def get(self, request):
        task_given_data =[];task_have_data = []
        core_obj = Core.objects.filter(user = request.user)
        cocom_obj = CoCom.objects.filter(user = request.user)
        for i in core_obj:
            task_given_obj = Task.objects.filter(assigned_by =i)
            task_given_data +=[{
                "Team Name" : x["team_assign"]["team_name"],
                "Task Name" : x["task_name"]
                } for x in TaskSerializer(task_given_obj, many=True).data]
        
        for i in cocom_obj:
            task_have_obj = AssignedTo.objects.filter(assgined_to =i)
            task_have_data += [{
                "Team Name" : x["task"]["team_assign"]["team_name"],
                "Task Name" : x["task"]["task_name"], 
                "Submitted" : x["submitted"], 
                "Assigned By": {
                    "First Name" : x["task"]["assigned_by"]["user"]["First_name"], 
                    "Last Name" : x["task"]["assigned_by"]["user"]["Last_name"]
                    }} for x in  AssignedToSerializer(task_have_obj, many=True).data]
            completed_task = [x for x in task_have_data if x["Submitted"] == True]
            incomplete_task = [x for x in task_have_data if x["Submitted"] == False]
        
        return Response({'status':200, 'payload':{'User': str(request.user),'task_given' : task_given_data ,'Completed Task': completed_task, "Incomplete Task":incomplete_task}})
  
class TeamApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]
    
    def delete(self, request, id = None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            team_committe_obj = Team.objects.get(id =id)
            team_committe_id = TeamSerializer(team_committe_obj).data['belongs_to']['id']
            if (team_committe_id in core_committee_id):
                team_committe_obj.delete()
                return Response({'status':200, 'payload': {'Team_id' : id}, 'message': 'Team Deleted Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Team\'s Committee','message' : 'Bad Request'})
        except Exception as e:
            return Response({'status': 403, 'message' : 'Invalid Id'})

    def patch(self, request, id = None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            team_committe_obj = Team.objects.get(id =id)
            team_committe_id = TeamSerializer(team_committe_obj).data['belongs_to']['id']
            if (team_committe_id in core_committee_id):
                try:
                    serializer = TeamSerializer(team_committe_obj, data = {'team_name' : request.data['team_name']}, partial =True)
                    if not serializer.is_valid():
                        return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                    serializer.save()
                except:
                    serializer = TeamSerializer(team_committe_obj)
                return Response({'status':200, 'payload': {'Team_id' : serializer.data['id']}, 'message': 'Team Updated Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except Exception as e:
            return Response({'status': 403, 'message' : 'Invalid Id'})

    def get(self, request):
        
        mentor_team_data=[];mentee_team_data=[]
        core_obj = Core.objects.filter(user = request.user)
        cocom_obj = CoCom.objects.filter(user = request.user)
        
        for i in core_obj:
            mentor_team_obj = Team.objects.filter(Mentors = i)
            mentor_team_data+=([{
                'Team Name' : x["team_name"], 
                'Belongs To' : x["belongs_to"]["Committee_name"], 
                'Mentors': [{
                    'First Name' : CoreSerializers(Core.objects.get(pk = y)).data['user']['First_name'], 
                    'Last Name' : CoreSerializers(Core.objects.get(pk = y)).data['user']['Last_name'], 
                    'Position' : CoreSerializers(Core.objects.get(pk = y)).data['position']['Position_name']} for y in x["Mentors"]],
                'Mentees': [{
                    'First Name' : CoComSerializers(CoCom.objects.get(pk = y)).data['user']['First_name'], 
                    'Last Name' : CoComSerializers(CoCom.objects.get(pk = y)).data['user']['Last_name'], 
                    'Position' : CoComSerializers(CoCom.objects.get(pk = y)).data['position']['Position_name']} for y in x["Mentee"]]    
                    } for x in TeamSerializer(mentor_team_obj, many=True).data])
        
        for i in cocom_obj:
            mentee_team_obj = Team.objects.filter(Mentee = i)
            # mentee_team_data += TeamSerializer(mentee_team_obj, many=True).data
            mentee_team_data+=([{
                'Team Name' : x["team_name"], 
                'Belongs To' : x["belongs_to"]["Committee_name"], 
                'Mentors': [{
                    'First Name' : CoreSerializers(Core.objects.get(pk = y)).data['user']['First_name'], 
                    'Last Name' : CoreSerializers(Core.objects.get(pk = y)).data['user']['Last_name'], 
                    'Position' : CoreSerializers(Core.objects.get(pk = y)).data['position']['Position_name']} for y in x["Mentors"]],
                'Mentees': [{
                    'First Name' : CoComSerializers(CoCom.objects.get(pk = y)).data['user']['First_name'], 
                    'Last Name' : CoComSerializers(CoCom.objects.get(pk = y)).data['user']['Last_name'], 
                    'Position' : CoComSerializers(CoCom.objects.get(pk = y)).data['position']['Position_name']} for y in x["Mentee"]]    
                    } for x in TeamSerializer(mentee_team_obj, many=True).data])
        
        return Response({'status':200, 'payload':{'User': str(request.user),'Teams(as Mentor)': mentor_team_data,'Teams(as Mentee)' :mentee_team_data}})

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

class TeamUpdateApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def patch(self, request, operation, id = None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            team_committe_obj = Team.objects.get(id =id)
            team_committe_id = TeamSerializer(team_committe_obj).data['belongs_to']['id']
            if (team_committe_id in core_committee_id):
                try:
                    team_Mentor = TeamSerializer(team_committe_obj).data['Mentors']
                    team_Mentee = TeamSerializer(team_committe_obj).data['Mentee']
                    
                    try:
                        mentor_list = request.data["Mentors"].strip('][}{)(').split(',')
                        core_list = [x['id'] for x in Core.objects.filter(committee = team_committe_id).values()]
                        for i in mentor_list:
                            if int(i) not in core_list:
                                return Response({'status': 403, 'error' : f"id : {i} is not in Committee's Core ",'message' : 'Bad Request'})
                    except:
                        mentor_list=[]

                    try:
                        mentee_list = request.data["Mentee"].strip('][}{)(').split(',')
                        cocom_list = [x['id'] for x in CoCom.objects.filter(committee = team_committe_id).values()]
                        for i in mentee_list:
                            if int(i) not in cocom_list:
                                return Response({'status': 403, 'error' : f"id : {i} is not in Committee's CoCom ",'message' : 'Bad Request'})
                    except:
                        mentee_list=[]

                    if(operation == 'add'):
                        serializer = TeamSerializer(team_committe_obj, data = {'Mentors' : team_Mentor + mentor_list, 'Mentee' : team_Mentee + mentee_list}, partial =True)
                        if not serializer.is_valid():
                            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                        serializer.save()
                    elif(operation == 'delete'):
                        mentor_list = list(map(int, mentor_list))
                        mentee_list = list(map(int, mentee_list))
                        serializer = TeamSerializer(team_committe_obj, data = {'Mentors' : list(set(team_Mentor) - set(mentor_list)), 'Mentee' : list(set(team_Mentee) - set(mentee_list))}, partial =True)
                        if not serializer.is_valid():
                            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                        serializer.save()
                    else:
                        return Response({'status':403, 'message': 'Allowed operations are [add, delete]'})
                except Exception as e:
                    serializer = TeamSerializer(team_committe_obj)
                return Response({'status':200, 'payload': {'Team_id' : serializer.data['id']}, 'message': 'Team Updated Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except Exception as e:
            return Response({'status': 403, 'message' : 'Invalid Id'})

class AssignedToApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def patch(self, request, id = None):
        try:
            assigned_obj = AssignedTo.objects.get(id = id)
            assigned_obj_user_id = AssignedToSerializer(assigned_obj).data["assgined_to"]["user"]["id"]
            if (request.user.id == assigned_obj_user_id):
                serializer = AssignedToSerializer(assigned_obj, data = request.data, partial = True)
                if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                serializer.save()
                return Response({'status':200, 'payload': {'Assgined To ID' : serializer.data['id']}, 'message': 'Assgined-Task Updated Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Current User ID Doesn\'t match with Assigned User ID','message' : 'Bad Request'})
        except:
            return Response({'status': 403, 'message' : 'Invalid Id'})