from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .services.analytics import (
    average_wait_for_stop,
    average_headway_for_line,
    line_status_from_incidents,
    stop_status_from_incidents
)

from .serializers_analytics import (
    AverageWaitSerializer,
    LineHeadwaySerializer,
    LineStatusSerializer
)

average_wait_example = {
    "stop_id": "940GZZLUBST",
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
            ),
            400: openapi.Response(
                description="Invalid stop ID",
                examples={"application/json": {"error": "Invalid stop ID"}}
            ),
            404: openapi.Response(
                description="Stop has no arrival data",
                examples={"application/json": {"detail": "Stop 'HUBZMG' not found or has no arrival data."}}
            ),
        }
    )
    def get(self, request, stop_id):
        error, avg = average_wait_for_stop(stop_id)
        
        # If avg is zero, treat as stop with no arrival data
        if avg == 0:
            raise NotFound(detail=f"Stop '{stop_id}' not found or has no arrival data.")
        
        if error:
            return Response(error, status=400)
        
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
                description="Successfully computed average headway for the line",
                examples={"application/json": line_headway_example}
            ),
            404: openapi.Response(
                description="Line not found or has insufficient arrival data",
                examples={"application/json": {"detail": "Line 'southern' not found or has insufficient arrival data."}}
            )  
        }
    )
    def get(self, request, line_id):
        headway = average_headway_for_line(line_id)
        
        if headway is None:
            raise NotFound(detail=f"Line '{line_id}' not found or has insufficient arrival data.")
        
        data = {"line_id": line_id, "average_headway_seconds": headway}
        return Response(data)

line_status_example = {
    "line_id": "victoria",
    "status": "Minor delays",
    "average_wait_seconds": 420.0
}

class LineIncidentStatusView(APIView):
    @swagger_auto_schema(
        operation_summary="Line status based on user incidents",
        operation_description="Computes the operational status of a line using recent user-reported incidents. The status is categorized based on the severity and number of incidents reported in the last 30 minutes.",
        tags=["Analytics - Lines"],
        responses={
            200: openapi.Response(
                description="Incident-based line status",
                examples={
                    "application/json": {
                        "line_id": "victoria",
                        "status": "Moderate delays",
                        "score": 5
                    }
                }
            )
        }
    )
    def get(self, request, line_id):
        status, score = line_status_from_incidents(line_id)
        return Response({
            "line_id": line_id,
            "status": status,
            "score": score
        })

class StopIncidentStatusView(APIView):
    @swagger_auto_schema(
        operation_summary="Stop status based on user incidents",
        operation_description="Computes the operational status of a stop using recent user-reported incidents. The status is categorized based on the severity and number of incidents reported in the last 30 minutes.",
        tags=["Analytics - Stops"],
        responses={
            200: openapi.Response(
                description="Incident-based stop status",
                examples={
                    "application/json": {
                        "stop_id": "940GZZLUBST",
                        "status": "Moderate issues",
                        "score": 5
                    }
                }
            )
        }
    )
    def get(self, request, stop_id):
        status, score = stop_status_from_incidents(stop_id)
        return Response({
            "stop_id": stop_id,
            "status": status,
            "score": score
        })