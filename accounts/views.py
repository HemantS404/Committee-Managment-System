from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.response import Response
import sys
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.forms.models import model_to_dict

class RegisterApi(APIView):
    def post(self, request):

        serializer = UserSerializers(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

        serializer.save()

        user = User.objects.get(email = serializer.data['email'])
        refresh = RefreshToken.for_user(user)

        return Response({'status': 200, 'payload' : {"User email" : serializer.data['email'] , "User id" : user.id},'message' : 'Registration Successful', 'refresh': str(refresh), 'access': str(refresh.access_token)})

class LogoutApi(APIView):
    def post(self, request):
        try:
            refresh_token  = request.data.get('refresh')
            if(refresh_token == None):
                return Response({'status':403, 'error': "refresh : This field is required."})
            else:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'status':200, 'message': 'Logout Successfully'})
        except :
            exc_type, value, traceback = sys.exc_info()
            return Response({'status':403, 'message': 'Some error has occured', 'error': exc_type.__name__})

class CommitteeRegisterApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):

        serializer = CommitteeSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
        serializer.save()

        position = PositionSerializer(data = {'Committee' : serializer.data['id'], 'Position_name' : 'Chairperson','Position_for' : 'Core'})
        if not position.is_valid():
            return Response({'status':403, 'errors': position.errors, 'message': 'Some error has occured'})
        position.save()
        
        chairperson = CoreSerializers(data ={'committee' : serializer.data['id'],'user' : request.user.id, 'position' : position.data['id']})
        if not chairperson.is_valid():
            return Response({'status':403, 'errors': chairperson.errors, 'message': 'Some error has occured'})
        chairperson.save()
        
        return Response({'status': 200, 'payload' : {"Committee_id" : serializer.data['id']},'message' : 'Committee Registered Successful'})

class PositionRegisterApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        
        try:
            if (int(request.data['Committee']) in core_committee_id):
                serializer = PositionSerializer(data = request.data)
                if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                serializer.save()
                return Response({'status': 200,  'payload' : {"Position_id" : serializer.data['id']},'message' : 'Position Registered Successful'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except:
            serializer = PositionSerializer(data = request.data)
            if not serializer.is_valid():
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

class GuideRegisterApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        
        try:
            
            if (int(request.data['committee']) in core_committee_id):
                serializer = GuideSerializers(data = request.data)
                if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                serializer.save()
                return Response({'status': 200,  'payload' : {"Guide_id" : serializer.data['id']},'message' : 'Guide Registered Successful'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except:
            serializer = GuideSerializers(data = request.data)
            if not serializer.is_valid():
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

class CoreRegisterApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        
        try:
            if (int(request.data['committee']) in core_committee_id):
                core_positions = [x['id'] for x in Position.objects.filter(Committee = request.data['committee'], Position_for = 'Core').values()]
                if(int(request.data['position']) in core_positions):
                    serializer = CoreSerializers(data = request.data)
                    if not serializer.is_valid():
                        return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                    serializer.save()
                    return Response({'status': 200,  'payload' : {"Core_id" : serializer.data['id']},'message' : 'Core Registered Successful'})
                else:
                    return Response({'status': 403, 'error' : 'Not a Core position in the Entered Committee','message' : 'Bad Request'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except:
            serializer = CoreSerializers(data = request.data)
            if not serializer.is_valid():
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

class CoComRegisterApi(GenericAPIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        
        try:
            if (int(request.data['committee']) in core_committee_id):
                cocom_positions = [x['id'] for x in Position.objects.filter(Committee = request.data['committee'], Position_for = 'CoCom').values()]
                if(int(request.data['position']) in cocom_positions):
                    serializer = CoComSerializers(data = request.data)
                    if not serializer.is_valid():
                        return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                    serializer.save()
                    return Response({'status': 200, 'payload' : {"CoCom_id" : serializer.data['id']},'message' : 'CoCom Registered Successful'})
                else:
                    return Response({'status': 403, 'error' : 'Not a CoCom position in the Entered Committee','message' : 'Bad Request'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except:
            serializer = CoComSerializers(data = request.data)
            if not serializer.is_valid():
                return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})