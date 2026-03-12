from rest_framework import serializers
from .models import UserRoute, UserStation, UserIncident, Stop, Line

class UserRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoute
        fields = "__all__"

class UserStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStation
        fields = "__all__"

class UserIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncident
        fields = "__all__"

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = "__all__"

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = "__all__"