from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from .models import UserRoute, UserStation, UserIncident, Stop, Line
from .serializers import (
    UserRouteSerializer,
    UserStationSerializer,
    UserIncidentSerializer,
    StopSerializer,
    LineSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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