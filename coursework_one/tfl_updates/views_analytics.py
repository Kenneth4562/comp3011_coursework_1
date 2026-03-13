from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services.analytics import (
    average_wait_for_stop,
    average_headway_for_line,
    line_status
)

from .serializers_analytics import (
    AverageWaitSerializer,
    LineHeadwaySerializer,
    LineStatusSerializer
)

average_wait_example = {
    "stop_id": "HUBZFD",
    "average_wait_seconds": 142.5
}

class StopAverageWaitView(APIView):
    @swagger_auto_schema(
        operation_summary="Compute average wait time for a stop",
        operation_description="Computes the average wait time (in seconds) for a specific stop based on current arrival data for the station (i.e., irrespective of the line, calculates the average wait).",
        tags=["Analytics - Stops"],
        responses={
            200: openapi.Response(
                description="Average wait time for the stop",
                examples={"application/json": average_wait_example}
            )
        }
    )
    def get(self, request, stop_id):
        avg = average_wait_for_stop(stop_id)
        data = {"stop_id": stop_id, "average_wait_seconds": avg}
        return Response(AverageWaitSerializer(data).data)

line_headway_example = {
    "line_id": "victoria",
    "average_headway_seconds": 180.0
}

class LineHeadwayView(APIView):
    @swagger_auto_schema(
        operation_summary="Compute average headway for a line",
        operation_description="Computes the average headway (time between consecutive services) for a line.",
        tags=["Analytics - Lines"],
        responses={
            200: openapi.Response(
                description="Average headway for the line",
                examples={"application/json": line_headway_example}
            )
        }
    )
    def get(self, request, line_id):
        headway = average_headway_for_line(line_id)
        data = {"line_id": line_id, "average_headway_seconds": headway}
        return Response(data)

line_status_example = {
    "line_id": "victoria",
    "status": "Minor delays",
    "average_wait_seconds": 420.0
}

class LineStatusView(APIView):
    @swagger_auto_schema(
        operation_summary="Determine the operational status of a line",
        operation_description="Determine the operational status of a line based on recent average wait times.",
        tags=["Analytics - Lines"],
        responses={
            200: openapi.Response(
                description="Status of the line",
                examples={"application/json": line_status_example}
            )
        }
    )
    def get(self, request, line_id):
        status, wait = line_status(line_id)
        data = {
            "line_id": line_id,
            "status": status,
            "average_wait_seconds": wait
        }
        return Response(data)
