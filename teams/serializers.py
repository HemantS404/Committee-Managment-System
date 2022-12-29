from rest_framework import serializers
from .models import *
from accounts.serializers import *

class TeamSerializer(serializers.ModelSerializer):
    # belongs_to = CommitteeSerializer(read_only =True)
    class Meta:
        model = Team
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['belongs_to'] = CommitteeSerializer(
            Committee.objects.get(pk=data['belongs_to'])).data
        return data

class TaskSerializer(serializers.ModelSerializer):
    # team_assign = TeamSerializer(read_only =True)
    # assigned_by = CoreSerializers(read_only =True)
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['team_assign'] = TeamSerializer(
            Team.objects.get(pk=data['team_assign'])).data
        data['assigned_by'] = CoreSerializers(
            Core.objects.get(pk=data['assigned_by'])).data
        return data

class AssignedToSerializer(serializers.ModelSerializer):
    # task = TaskSerializer(read_only =True)
    # assgined_to = CoComSerializers(read_only =True)
    class Meta:
        model = AssignedTo
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['task'] = TaskSerializer(
            Task.objects.get(pk=data['task'])).data
        data['assgined_to'] = CoComSerializers(
            CoCom.objects.get(pk=data['assgined_to'])).data
        return data