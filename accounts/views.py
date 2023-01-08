from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework.response import Response
import sys
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from django.core.mail import send_mail
from .custompermission import IsVerified
from uuid import uuid4
from twilio.rest import Client

class RegisterApi(APIView):
    def get(self, request, id, token):
        try:
            user_obj = User.objects.get(id = id)
            user_data = UserSerializers(user_obj).data
            if(token == user_data['email_token']):
                user_obj.is_email_verified = True
                user_obj.save()
                return HttpResponse('<h1>User is Verified Successfully</h1>')
            else:
                return HttpResponse('<h1>Token is not valid</h1>')
        except:
            return HttpResponse('<h1>Sorry Some error has occured</h1>')

    def post(self, request):

        serializer = UserSerializers(data = request.data)

        if not serializer.is_valid():
            return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})

        serializer.save()
        user_data = serializer.data
        try:
            subject = 'Welcome to Committee Managment System'
            message = f'Hi!\n{user_data["First_name"]} {user_data["Last_name"]}, thank you for registering in Committee Managment System.\nPlease Click here to verfy Your Account http://127.0.0.1:8000/accounts/verify/{user_data["id"]}/{user_data["email_token"]}/\nThis is a Computer generated mail don\'t reply to this mail'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user_data['email'], ]
            send_mail( subject, message, email_from, recipient_list )
        except:
            return Response({'status': 403, 'message': 'Sorry Some error has occured'})
        try:
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                                        body=f'Your OTP - {user_data["phone_otp"]}',
                                        from_=settings.TWILIO_PHONE,
                                        to=user_data['phone']
                                    )

            print(message.sid)
        except:
            return Response({'status': 403, 'message': 'Sorry Some error has occured'})

        user = User.objects.get(email = user_data['email'])
        refresh = RefreshToken.for_user(user)

        return Response({'status': 200, 'payload' : {"User email" : user_data['email'] , "User id" : user.id},'message' : 'Registration Successful, Please Check Your Mail, an Email verfication link has been provided, an OTP has been send to your number', 'refresh': str(refresh), 'access': str(refresh.access_token)})

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

class CommitteeApi(GenericAPIView):
    serializer_class = CoComSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]
    
    def delete(self, request, id=None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            committee_obj = Committee.objects.get(id =id)
            if (int(id) in core_committee_id):
                committee_obj.delete()
                return Response({'status': 200, 'payload' : {"Committee_id" : id},'message' : 'Committee Deleted Successful'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except:
            return Response({'status': 403, 'message' : 'Invalid Id'})

    def patch(self, request, id=None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            committee_obj = Committee.objects.get(id =id)
            if (int(id) in core_committee_id):
                serializer = CommitteeSerializer(committee_obj, data = request.data, partial =True)
                if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                serializer.save()
                return Response({'status': 200, 'payload' : {"Committee_id" : serializer.data['id']},'message' : 'Committee Updated Successful'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Committee','message' : 'Bad Request'})
        except:
            return Response({'status': 403, 'message' : 'Invalid Id'})

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

class PositionApi(GenericAPIView):
    serializer_class = PositionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def delete(self, request, id=None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            position_obj = Position.objects.get(id =id)
            position_committee = PositionSerializer(position_obj).data['Committee']['id']
            if (position_committee in core_committee_id):
                position_obj.delete()
                return Response({'status': 200, 'payload' : {"Position_id" : id},'message' : 'Position Deleted Successful'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Position\'s Committee','message' : 'Bad Request'})
        except:
            return Response({'status': 403, 'message' : 'Invalid Id'})

    def patch(self, request, id=None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()]
        try:
            position_obj = Position.objects.get(id =id)
            position_committee = PositionSerializer(position_obj).data['Committee']['id']
            if (position_committee in core_committee_id):
                serializer = PositionSerializer(position_obj, data = request.data, partial =True)
                if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
                serializer.save()
                return Response({'status': 200, 'payload' : {"Position_id" : serializer.data['id']},'message' : 'Position Updated Successful'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Position\'s Committee','message' : 'Bad Request'})
        except:
            return Response({'status': 403, 'message' : 'Invalid Id'})

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

class GuideApi(GenericAPIView):
    serializer_class = GuideSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]
    
    def delete(self, request, id = None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()] 
        try:
            guide_obj = Guide.objects.get(id =id)
            guide_committee_id = GuideSerializers(guide_obj).data["committee"]["id"]
            if (guide_committee_id in core_committee_id):
                guide_obj.delete()
                return Response({'status': 403, 'payload': {'Guide Id' : id},'message' : 'Guide Deleted Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Guide\'s Committee','message' : 'Bad Request'})
        except Exception as e:
            print(e)
            return Response({'status':403,'message': 'Invalid ID'})

    def get(self, request):
        guide_obj = Guide.objects.filter(user = request.user)
        guide_data = [{"Committee" : x["committee"]["Committee_name"], 'Designation' : x['designation']} for x in GuideSerializers(guide_obj, many=True).data]
        return Response({'status': 200, 'payload':{'User': str(request.user),'Guide': guide_data}})

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

class CoreApi(GenericAPIView):
    serializer_class = CoreSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]
    
    def delete(self, request, id = None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()] 
        try:
            core_obj = Core.objects.get(id =id)
            core_committee_id_enter = CoreSerializers(core_obj).data["committee"]["id"]
            if (core_committee_id_enter in core_committee_id):
                core_obj.delete()
                return Response({'status': 403, 'payload': {'Core Id' : id},'message' : 'Core Deleted Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered Core\'s Committee','message' : 'Bad Request'})
        except:
            return Response({'status':403,'message': 'Invalid ID'})

    def get(self, request):
        core_obj = Core.objects.filter(user = request.user)
        core_data = [{"committee" : x["committee"]["Committee_name"], "position" : x["position"]["Position_name"]} for x in CoreSerializers(core_obj, many=True).data]
        return Response({'status': 200, 'payload':{'User': str(request.user),'Core': core_data}})

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

class CoComApi(GenericAPIView):
    serializer_class = CoComSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def delete(self, request, id = None):
        core_committee_id = [x['committee_id'] for x in Core.objects.filter(user = request.user).values()] 
        try:
            cocom_obj = CoCom.objects.get(id =id)
            cocom_committee_id = CoComSerializers(cocom_obj).data["committee"]["id"]
            if (cocom_committee_id in core_committee_id):
                cocom_obj.delete()
                return Response({'status': 403, 'payload': {'CoCom Id' : id},'message' : 'CoCom Deleted Successfully'})
            else:
                return Response({'status': 403, 'error' : 'Not a Core in the Entered CoCom\'s Committee','message' : 'Bad Request'})
        except:
            return Response({'status':403,'message': 'Invalid ID'})

    def get(self, request):
        cocom_obj = CoCom.objects.filter(user = request.user)
        cocom_data = [{"committee" : x["committee"]["Committee_name"], "position" : x["position"]["Position_name"]} for x in CoComSerializers(cocom_obj, many=True).data]
        return Response({'status': 200, 'payload':{'User': str(request.user),'CoCom': cocom_data}})
    
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

class UserApi(GenericAPIView):
    serializer_class = UserSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def delete(self, request):
        user_obj = User.objects.get(id=request.user.id)
        id = request.user.id
        user_obj.delete()
        return Response({'status':200, 'payload': {'User_id' : id}, 'message': 'User Deleted Successfully'})

    def patch(self, request):
        try:
            dicty = {}
            flag = 0 
            for arr in request.data:
                if arr == 'password':
                    flag = 1
                    password = request.data[arr]
                else:
                    dicty[arr] = request.data[arr]
            user_obj = User.objects.get(id=request.user.id)
            serializer =  UserSerializers(user_obj, data = dicty, partial =True)
            if not serializer.is_valid():
                    return Response({'status':403, 'errors': serializer.errors, 'message': 'Some error has occured'})
            if flag == 1:    
                user_obj.set_password(password)
            serializer.save()
            return Response({'status':200, 'payload': {'User_id' : serializer.data['id']}, 'message': 'User Updated Successfully'})
        except Exception as e:
            print(e)
            return Response({'status': 403, 'message' : e})
     
class PasswordResetApi(GenericAPIView):
    serializer_class = UserSerializers
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsVerified]

    def get(self, request):
        user_obj = User.objects.get(id=request.user.id)
        user_data = UserSerializers(user_obj).data
        subject = 'Password Reset Mail'
        uuid = uuid4()
        user_obj.password_reset_token = uuid
        user_obj.save()
        message = f'http://127.0.0.1:8000/accounts/redirect/{user_data["id"]}/{uuid}/'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user_data['email'], ]
        send_mail( subject, message, email_from, recipient_list )
        return Response({'status': 200, 'message' : 'Please check your mail a password reset link has been provided'})
    
def reset(request, id, token):
    
    if request.method == 'GET':
        user_obj = User.objects.get(id=id)
        if(token == user_obj.password_reset_token):
            return render(request, "passwordreset.html", {'id' : id, 'token' : token})
        else:
            return HttpResponse('<h1>Token is not valid</h1>')
    elif request.method == 'POST':
        password = request.POST['password']
        user_obj = User.objects.get(id=id)
        if(token == user_obj.password_reset_token):
            try:
                user_obj.set_password(password)
                user_obj.save()
                return HttpResponse('<h1>User Password changed Successfully</h1>')
            except:
                return HttpResponse('<h1>Some error has occured</h1>')
        else:
            return HttpResponse('<h1>Token is not valid</h1>')

def otpVerify(request, id):
    try:
        if request.method == 'GET':
            user_obj = User.objects.get(id=id)
            return render(request, "otpverify.html", {'id' : id})
        elif request.method == 'POST':
            otp = request.POST['otp']
            user_obj = User.objects.get(id=id)
            if(int(otp) == int(user_obj.phone_otp)):
                try:
                    user_obj.is_phone_verified =True
                    user_obj.save()
                    return HttpResponse('<h1>User Phone number is Verified Successfully</h1>')
                except:
                    return HttpResponse('<h1>Some error has occured</h1>')
            else:
                return HttpResponse('<h1>Wrong OTP</h1>')
    except:
        return HttpResponse('<h1>Wrong ID</h1>')