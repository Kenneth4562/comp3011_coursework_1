from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import ArrivalRecord, UserRoute, UserStation, UserIncident, Stop, Line
from .serializers import (
    ArrivalRecordSerializer,
    UserRouteSerializer,
    UserStationSerializer,
    UserIncidentSerializer,
    StopSerializer,
    LineSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import APIView, swagger_auto_schema
from drf_yasg import openapi
from tfl_updates.services.tfl_client import get_arrivals_for_stop
from tfl_updates.services.arrival_transformer import transform_arrival
from tfl_updates.services.arrival_saver import save_arrival

# Create your views here.

### USER ROUTES
class UserRouteListCreateView(generics.ListCreateAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve all user routes",
        operation_description="Retrieve all user-added/favourite routes.",
        tags=["User Routes"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a new favourite route",
        operation_description="Adds a new route for a user, including origin stop, destination stop, and line.",
        tags=["User Routes"],
        request_body=UserRouteSerializer,
        responses={
            201: openapi.Response(
                description="Route created successfully",
                examples={
                    "application/json": {
                        "id": 12,
                        "user": 1,
                        "from_stop": "490008660N",
                        "to_stop": "490008661S",
                        "line": "victoria"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserRouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve a user route",
        operation_description="Retrieve a specific user route",
        tags=["User Routes"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a user route",
        operation_description="Update a specific user route",
        tags=["User Routes"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a user route",
        operation_description="Partially update a specific user route",
        tags=["User Routes"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a user route",
        operation_description="Delete a specific user route",
        tags=["User Routes"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

### USER STATIONS
class UserStationListCreateView(generics.ListCreateAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve all favourite stations",
        operation_description="Retrieve all favourite stations for all users",
        tags=["User Stations"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a favourite station",
        operation_description="Marks a stop as a favourite for a user.",
        tags=["User Stations"],
        request_body=UserStationSerializer,
        responses={
            201: openapi.Response(
                description="Favourite station added",
                examples={
                    "application/json": {
                        "id": 5,
                        "user": 1,
                        "stop": "HUBZFD"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserStationDetailView(generics.RetrieveDestroyAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve a specific favourite station",
        operation_description="Retrieve a specific favourite station for a user",
        tags=["User Stations"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a favourite station",
        operation_description="Delete a specific favourite station for a user",
        tags=["User Stations"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

### USER INCIDENTS
class UserIncidentListCreateView(generics.ListCreateAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve all user-reported incidents",
        operation_description="Retrieve all user-reported incidents",
        tags=["User Incidents"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Report a user incident",
        operation_description="Creates a new incident report for a stop and line.",
        tags=["User Incidents"],
        request_body=UserIncidentSerializer,
        responses={
            201: openapi.Response(
                description="Incident created",
                examples={
                    "application/json": {
                        "id": 3,
                        "user": 1,
                        "stop": "HUBZFD",
                        "line": "victoria",
                        "description": "Severe delays, platform overcrowded",
                        "severity": 4
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserIncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer

    @swagger_auto_schema(
        operation_summary="Retrieve a specific incident",
        operation_description="Retrieve a specific incident",
        tags=["User Incidents"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a specific incident",
        operation_description="Update a specific incident",
        tags=["User Incidents"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a specific incident",
        operation_description="Partially update a specific incident",
        tags=["User Incidents"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a specific incident",
        operation_description="Delete a specific incident",
        tags=["User Incidents"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

### STOPS AND LINES
class StopListView(generics.ListAPIView):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["mode"]
    @swagger_auto_schema(
        operation_summary="Retrieve all stops in the database",
        operation_description="Retrieve all stops in the database. Supports filtering by mode (e.g. tube, elizabeth-line, dlr, overground, tram).",
        tags=["Stops"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class LineListView(generics.ListAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    @swagger_auto_schema(
        operation_summary="Retrieve all lines in the database",
        operation_description="Retrieve all lines in the database.",
        tags=["Lines"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

arrivals_example = [
    {
        "stop": "HUBZFD",
        "line": "victoria",
        "predicted_time": "2026-03-13T10:05:00Z",
        "time_to_station": 120
    }
]

class StopArrivalsView(APIView):

    @swagger_auto_schema(
        operation_summary="Retrieve arrival predictions for a stop",
        operation_description="Retrieve arrival predictions for a stop. Use ?refresh=true to fetch fresh data from TfL.",
        tags=["Arrivals"],
        manual_parameters=[
            openapi.Parameter(
                'refresh',
                openapi.IN_QUERY,
                description="If true, fetch fresh arrival data from TfL before returning results.",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: openapi.Response(
                description="List of arrival predictions",
                examples={"application/json": arrivals_example}
            )
        }
    )
    def get(self, request, stop_id):
        refresh_param = request.GET.get("refresh", "").lower()
        refresh = refresh_param in ["true", "1", "yes"]

        if refresh:
            arrivals = get_arrivals_for_stop(stop_id)
            for item in arrivals:
                data = transform_arrival(item)
                save_arrival(data)

        records = ArrivalRecord.objects.filter(stop_id=stop_id)
        serializer = ArrivalRecordSerializer(records, many=True)
        return Response(serializer.data)