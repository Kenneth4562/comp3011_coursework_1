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

# Create your views here.
""" def HandleRegisterRequest(request):
    return HttpResponse("not yet implemented") """

class UserRouteListCreateView(generics.ListCreateAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

class UserRouteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserRoute.objects.all()
    serializer_class = UserRouteSerializer

class UserStationListCreateView(generics.ListCreateAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer

class UserStationDetailView(generics.RetrieveDestroyAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer

class UserIncidentListCreateView(generics.ListCreateAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer

class UserIncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer

class StopListView(generics.ListAPIView):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["mode"]


class LineListView(generics.ListAPIView):
    """
    Retrieve all lines in the database.
    """
    queryset = Line.objects.all()
    serializer_class = LineSerializer