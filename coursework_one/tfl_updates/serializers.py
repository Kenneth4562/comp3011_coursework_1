from rest_framework import serializers
from .models import UserRoute, UserStation, UserIncident, Stop, Line, ArrivalRecord

class ArrivalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalRecord
        fields = "__all__"

class UserRouteSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(
        help_text="ID of the user creating the route",
        min_value=1,
        error_messages={
            "required": "User ID is required.",
            "invalid": "User ID must be an integer.",
            "min_value": "User ID must be positive."
        }
    )

    from_stop = serializers.CharField(
        help_text="Origin stop ID",
        max_length=20,
        error_messages={
            "required": "Origin stop ID is required.",
            "max_length": "Stop ID cannot exceed 20 characters."
        }
    )

    to_stop = serializers.CharField(
        help_text="Destination stop ID",
        max_length=20,
        error_messages={
            "required": "Destination stop ID is required.",
            "max_length": "Stop ID cannot exceed 20 characters."
        }
    )

    line = serializers.CharField(
        help_text="Line ID for the route",
        max_length=20,
        error_messages={
            "required": "Line ID is required.",
            "max_length": "Line ID cannot exceed 20 characters."
        }
    )

    class Meta:
        model = UserRoute
        fields = "__all__"

class UserStationSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(
        help_text="ID of the user",
        min_value=1,
        error_messages={
            "required": "User ID is required.",
            "invalid": "User ID must be an integer."
        }
    )

    stop = serializers.CharField(
        help_text="Stop ID to mark as favourite",
        max_length=20,
        error_messages={
            "required": "Stop ID is required.",
            "max_length": "Stop ID cannot exceed 20 characters."
        }
    )

    class Meta:
        model = UserStation
        fields = "__all__"

class UserIncidentSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(
        help_text="ID of the user reporting the incident",
        min_value=1,
        error_messages={
            "required": "User ID is required.",
            "invalid": "User ID must be an integer."
        }
    )

    stop = serializers.CharField(
        help_text="Stop ID where the incident occurred",
        max_length=20,
        error_messages={
            "required": "Stop ID is required.",
            "max_length": "Stop ID cannot exceed 20 characters."
        }
    )

    line = serializers.CharField(
        help_text="Line ID affected by the incident",
        max_length=20,
        error_messages={
            "required": "Line ID is required.",
            "max_length": "Line ID cannot exceed 20 characters."
        }
    )

    description = serializers.CharField(
        help_text="Description of the incident",
        max_length=200,
        error_messages={
            "required": "Description is required.",
            "max_length": "Description cannot exceed 200 characters."
        }
    )

    severity = serializers.IntegerField(
        help_text="Severity level (1–5)",
        min_value=1,
        max_value=5,
        error_messages={
            "required": "Severity is required.",
            "invalid": "Severity must be an integer.",
            "min_value": "Severity must be at least 1.",
            "max_value": "Severity cannot exceed 5."
        }
    )

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