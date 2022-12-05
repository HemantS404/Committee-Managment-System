from rest_framework import serializers
from .models import *

class RegisterSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['Department', 
            'First_name', 
            'Last_name', 
            'date_of_birth',
            'phone',
            'email',
            'password']

    def validate(self, data):
        for i in data['First_name'] :
            if i.isdigit():
                raise serializers.ValidationError({'error':'Name cannot have digits'})
        for i in data['Last_name'] :
            if i.isdigit():
                raise serializers.ValidationError({'error':'Name cannot have digits'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            Department = validated_data['Department'], 
            First_name = validated_data['First_name'], 
            Last_name = validated_data['Last_name'], 
            date_of_birth = validated_data['date_of_birth'],
            phone = validated_data['phone'],
            email = validated_data['email'],
            )
        user.set_password(validated_data['password'])
        user.save()
        return user

        
    
   
    
    
    