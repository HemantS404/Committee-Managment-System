from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.response import Response

class RegisterApi(APIView):
    def post(self, request):

        serializer = RegisterSerializers(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

        serializer.save()

        user = User.objects.get(email = serializer.data['email'])
        refresh = RefreshToken.for_user(user)

        return Response({'status': 200, 'message' : 'Registration Successful', 'refresh': str(refresh), 'access': str(refresh.access_token)})

class LogoutApi(APIView):
    def post(self, request):
        try:
            refresh_token  = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'status':200, 'message': 'Logout Successfully'})
        except :
            return Response({'status':403, 'message': 'Some error has occured'})