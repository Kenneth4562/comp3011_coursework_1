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
""" def HandleRegisterRequest(request):
    return HttpResponse("not yet implemented") """

class UserRouteListCreateView(generics.ListCreateAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

    @swagger_auto_schema(
        operation_description="Retrieve all user routes",
        tags=["User Routes"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user route",
        tags=["User Routes"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserRouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a specific user route",
        tags=["User Routes"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific user route",
        tags=["User Routes"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific user route",
        tags=["User Routes"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific user route",
        tags=["User Routes"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UserStationListCreateView(generics.ListCreateAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer

    @swagger_auto_schema(
        operation_description="Retrieve all favourite stations for all users",
        tags=["User Stations"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Add a new favourite station for a user",
        tags=["User Stations"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserStationDetailView(generics.RetrieveDestroyAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a specific favourite station",
        tags=["User Stations"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a favourite station",
        tags=["User Stations"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class UserIncidentListCreateView(generics.ListCreateAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer

    @swagger_auto_schema(
        operation_description="Retrieve all user-reported incidents",
        tags=["User Incidents"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user-reported incident",
        tags=["User Incidents"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserIncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer

    @swagger_auto_schema(
        operation_description="Retrieve a specific incident",
        tags=["User Incidents"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific incident",
        tags=["User Incidents"]
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a specific incident",
        tags=["User Incidents"]
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific incident",
        tags=["User Incidents"]
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class StopListView(generics.ListAPIView):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["mode"]
    @swagger_auto_schema(
        operation_description="Retrieve all stops in the database. Supports filtering by mode (e.g. tube, elizabeth-line, dlr, overground, tram).",
        tags=["Stops"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class LineListView(generics.ListAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    @swagger_auto_schema(
        operation_description="Retrieve all lines in the database.",
        tags=["Lines"]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
class StopArrivalsView(APIView):
    refresh_param = openapi.Parameter(
        'refresh',
        openapi.IN_QUERY,
        description="If true, fetch fresh arrival data from TfL before returning results",
        type=openapi.TYPE_BOOLEAN
    )
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'refresh',
                openapi.IN_QUERY,
                description="If true, fetch fresh arrival data from TfL before returning results",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        operation_description="Retrieve arrival predictions for a stop. Use ?refresh=true to fetch new data from TfL.",
        tags=["Arrivals"]
    )
    
    def get(self, request, stop_id):
        refresh = request.GET.get("refresh") == "true"

        if refresh:
            arrivals = get_arrivals_for_stop(stop_id)
            for item in arrivals:
                data = transform_arrival(item)
                save_arrival(data)

        # return latest stored arrivals
        records = ArrivalRecord.objects.filter(stop_id=stop_id)
        serializer = ArrivalRecordSerializer(records, many=True)
        return Response(serializer.data)