from rest_framework import serializers

class AverageWaitSerializer(serializers.Serializer):
    stop_id = serializers.CharField()
    average_wait_seconds = serializers.FloatField()

class LineHeadwaySerializer(serializers.Serializer):
    line_id = serializers.CharField()
    average_headway_seconds = serializers.FloatField()

class LineStatusSerializer(serializers.Serializer):
    line_id = serializers.CharField()
    status = serializers.CharField()
    average_wait_seconds = serializers.FloatField()
