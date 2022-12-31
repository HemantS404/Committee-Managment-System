from rest_framework import serializers
from .models import *
from uuid import uuid4

class CommitteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Committee
        fields ='__all__'

class PositionSerializer(serializers.ModelSerializer):
    # Committee = CommitteeSerializer(read_only =True)
    class Meta:
        model = Position
        fields ='__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['Committee'] = CommitteeSerializer(
            Committee.objects.get(pk=data['Committee'])).data
        return data

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def validate(self, data):
        try:
            for i in data['First_name'] :
                if i.isdigit():
                    raise serializers.ValidationError({'error':'Name cannot have digits'})
            for i in data['Last_name'] :
                if i.isdigit():
                    raise serializers.ValidationError({'error':'Name cannot have digits'})
            return data
        except:
            return data
        
    
    def create(self, validated_data):
        user = User.objects.create( 
            First_name = validated_data['First_name'], 
            Last_name = validated_data['Last_name'], 
            date_of_birth = validated_data['date_of_birth'],
            phone = validated_data['phone'],
            email = validated_data['email'],
            department = validated_data['department'],
            email_token = uuid4(),
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GuideSerializers(serializers.ModelSerializer):
    # committee = CommitteeSerializer(read_only =True)
    # user = UserSerializers(read_only =True)
    class Meta:
        model = Guide
        fields ='__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['committee'] = CommitteeSerializer(
            Committee.objects.get(pk=data['committee'])).data
        data['user'] = UserSerializers(
            User.objects.get(pk=data['user'])).data
        return data
        
class CoreSerializers(serializers.ModelSerializer):
    # committee = CommitteeSerializer(read_only =True)
    # user = UserSerializers(read_only =True)
    # position = PositionSerializer(read_only =True)
    class Meta:
        model = Core
        fields ='__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['committee'] = CommitteeSerializer(
            Committee.objects.get(pk=data['committee'])).data
        data['user'] = UserSerializers(
            User.objects.get(pk=data['user'])).data
        data['position'] = PositionSerializer(
            Position.objects.get(pk=data['position'])).data
        return data

class CoComSerializers(serializers.ModelSerializer):
    # committee = CommitteeSerializer(read_only =True)
    # user = UserSerializers(read_only =True)
    # position = PositionSerializer(read_only =True)
    class Meta:
        model = CoCom
        fields ='__all__'
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['committee'] = CommitteeSerializer(
            Committee.objects.get(pk=data['committee'])).data
        data['user'] = UserSerializers(
            User.objects.get(pk=data['user'])).data
        data['position'] = PositionSerializer(
            Position.objects.get(pk=data['position'])).data
        return data
    