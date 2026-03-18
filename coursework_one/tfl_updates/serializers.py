from rest_framework import serializers
from .models import UserRoute, UserStation, UserIncident, Stop, Line, ArrivalRecord
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class ArrivalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArrivalRecord
        fields = "__all__"

class UserRouteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    
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
        fields = ["id", "user", "from_stop", "to_stop", "line"]
        read_only_fields = ["user"]
        
    # Helper methods to convert IDs → objects for create/update operations
    def _get_stop(self, stop_id, field_name):
        try:
            return Stop.objects.get(stop_id=stop_id)
        except Stop.DoesNotExist:
            raise serializers.ValidationError({field_name: "Stop ID does not exist."})

    def _get_line(self, line_id):
        try:
            return Line.objects.get(line_id=line_id)
        except Line.DoesNotExist:
            raise serializers.ValidationError({"line": "Line ID does not exist."})
    
    # Override create to handle conversion of stop/line IDs to objects and validation
    def create(self, validated_data):
        # Convert IDs → objects
        if "from_stop" in validated_data:
            validated_data["from_stop"] = self._get_stop(validated_data["from_stop"], "from_stop")

        if "to_stop" in validated_data:
            validated_data["to_stop"] = self._get_stop(validated_data["to_stop"], "to_stop")

        if "line" in validated_data:
            validated_data["line"] = self._get_line(validated_data["line"])

        return UserRoute.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # Convert IDs → objects
        if "from_stop" in validated_data:
            validated_data["from_stop"] = self._get_stop(validated_data["from_stop"], "from_stop")

        if "to_stop" in validated_data:
            validated_data["to_stop"] = self._get_stop(validated_data["to_stop"], "to_stop")

        if "line" in validated_data:
            validated_data["line"] = self._get_line(validated_data["line"])

        return super().update(instance, validated_data)

class UserStationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
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
        fields = ["id", "user", "stop"]
        read_only_fields = ["user"]
        
    def create(self, validated_data):
        stop_id = validated_data.pop("stop")

        try:
            stop_obj = Stop.objects.get(stop_id=stop_id)
        except Stop.DoesNotExist:
            raise serializers.ValidationError({"stop": "Stop ID does not exist."})

        return UserStation.objects.create(stop=stop_obj, **validated_data)

class UserIncidentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    
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
        help_text="Severity level (1-5)",
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
        fields = ["id", "user", "stop", "line", "description", "severity"]
        read_only_fields = ["user"]
    
    def create(self, validated_data):
        stop_id = validated_data.pop("stop")
        line_id = validated_data.pop("line")

        try:
            stop_obj = Stop.objects.get(stop_id=stop_id)
        except Stop.DoesNotExist:
            raise serializers.ValidationError({"stop": "Stop ID does not exist."})

        try:
            line_obj = Line.objects.get(line_id=line_id)
        except Line.DoesNotExist:
            raise serializers.ValidationError({"line": "Line ID does not exist."})

        return UserIncident.objects.create(
            stop=stop_obj,
            line=line_obj,
            **validated_data
        )

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = "__all__"

class LineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Line
        fields = "__all__"