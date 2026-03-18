from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve all user routes",
        operation_description="Retrieve all user-added/favourite routes.",
        tags=["User Routes"],
        responses={
            200: openapi.Response(
                description="List of user routes",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "user": "John Doe",
                            "from_stop": "Farringdon (HUBZFD)",
                            "to_stop": "Whitechapel (HUBZWL)",
                            "line": "Elizabeth line"
                        },
                        {
                            "id": 2,
                            "user": "Jane Smith",
                            "from_stop": "Ealing Broadway (HUBEAL)",
                            "to_stop": "Liverpool Street (HUBZLST)",
                            "line": "Central line"
                        }
                    ]
                }
            )
        }
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
                        "user": "John Doe",
                        "from_stop": "Farringdon (HUBZFD)",
                        "to_stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line"
                    }
                }
            ), 
            400: openapi.Response(
                description="Invalid input data",
                examples={
                    "application/json": {
                        "from_stop": "Stop ID does not exist."
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve a user route",
        operation_description="Retrieve a specific user route by its ID.",
        tags=["User Routes"],
        responses={
            200: openapi.Response(
                description="User route details",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "from_stop": "Farringdon (HUBZFD)",
                        "to_stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line"
                    }
                }
            ),
            404: openapi.Response(
                description="Route not found",
                examples={"application/json": {"error": "User route not found"}}
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a user route",
        operation_description="Update a specific user route",
        tags=["User Routes"],
        request_body=UserRouteSerializer,
        responses={
            200: openapi.Response(
                description="Route updated successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "from_stop": "Farringdon (HUBZFD)",
                        "to_stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line"
                    }
                }
            ), 
            400: openapi.Response(
                description="Invalid input data",
                examples={
                    "application/json": {
                        "from_stop": "Stop ID does not exist."
                    }
                }
            ),
            404: openapi.Response(
                description="Route not found",
                examples={"application/json": {"detail": "No UserRoute matches the given query."}}
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a user route",
        operation_description="Partially update a specific user route. Only the updated fields need to be provided in the request body.",
        tags=["User Routes"],
        request_body=UserRouteSerializer,
        responses={
            200: openapi.Response(
                description="Route partially updated successfully",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "from_stop": "Farringdon (HUBZFD)",
                        "to_stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line"
                    }
                }
            ), 
            400: openapi.Response(
                description="Invalid input data",
                examples={
                    "application/json": {
                        "from_stop": "Stop ID does not exist."
                    }
                }
            ),
            404: openapi.Response(
                description="Route not found",
                examples={"application/json": {"detail": "No UserRoute matches the given query."}}
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a user route",
        operation_description="Delete a specific user route",
        tags=["User Routes"],
        responses={
            204: openapi.Response(
                description="Route deleted successfully",
                examples=None
            ),
            404: openapi.Response(
                description="Route not found",
                examples={"application/json": {"detail": "No UserRoute matches the given query."}}
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

### USER STOPS
class UserStationListCreateView(generics.ListCreateAPIView):
    queryset = UserStation.objects.all()
    serializer_class = UserStationSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve all favourite stops",
        operation_description="Retrieve all favourite stops for all users",
        tags=["User Stops"],
        responses={
            200: openapi.Response(
                description="List of user favourite stops. Returns empty list if no favourite stops added.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "user": "John Doe",
                            "stop": "Farringdon (HUBZFD)"
                        },
                        {
                            "id": 2,
                            "user": "Jane Smith",
                            "stop": "Whitechapel (HUBZWL)"
                        }
                    ]
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Add a favourite stop",
        operation_description="Marks a stop as a favourite for a user.",
        tags=["User Stops"],
        request_body=UserStationSerializer,
        responses={
            201: openapi.Response(
                description="Favourite stop added",
                examples={
                    "application/json": {
                        "id": 5,
                        "user": "John Doe",
                        "stop": "Farringdon (HUBZFD)"
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
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific favourite stop",
        operation_description="Retrieve a specific favourite stop for a user",
        tags=["User Stops"],
        responses={
            200: openapi.Response(
                description="Favourite stop details",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "stop": "Farringdon (HUBZFD)"
                    }
                }
            ), 
            404: openapi.Response(
                description="Favourite stop not found",
                examples={"application/json": {"detail": "No UserStation matches the given query."}}
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a favourite stop",
        operation_description="Delete a specific favourite stop for a user",
        tags=["User Stops"],
        responses={
            204: openapi.Response(
                description="Favourite stop deleted successfully",
            ), 
            404: openapi.Response(
                description="Favourite stop not found",
                examples={"application/json": {"detail": "No UserStation matches the given query."}}
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

### USER INCIDENTS
class UserIncidentListCreateView(generics.ListCreateAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve all user-reported incidents",
        operation_description="Retrieves all user-reported incidents.",
        tags=["User Incidents"],
        responses={
            200: openapi.Response(
                description="List of user incidents. Returns empty list if no issues reported.",
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "user": "John Doe",
                            "stop": "Whitechapel (HUBZWL)",
                            "line": "Elizabeth line",
                            "description": "Severe delays, platform overcrowded",
                            "severity": 4,
                            "created_at": "2026-03-12T17:30:00Z"
                        },
                        {
                            "id": 2,
                            "user": "Jane Smith",
                            "stop": "Liverpool Street (HUBZLST)",
                            "line": "Central line",
                            "description": "Minor delays, train at full capacity",
                            "severity": 2,
                            "created_at": "2026-03-12T16:45:00Z"
                        }
                    ]
                }
            )
        }
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
                        "user": "John Doe",
                        "stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line",
                        "description": "Severe delays, platform overcrowded",
                        "severity": 4
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid input data",
                examples={"application/json": {"line": "Line ID does not exist."}}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserIncidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserIncident.objects.all()
    serializer_class = UserIncidentSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_summary="Retrieve a specific incident",
        operation_description="Retrieve a specific incident from a given Incident ID. Example: ID = 1",
        tags=["User Incidents"],
        responses={
            200: openapi.Response(
                description="Incident details",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line",
                        "description": "Severe delays, platform overcrowded",
                        "severity": 4,
                        "created_at": "2026-03-12T17:30:00Z"
                    }
                }
            ), 
            404: openapi.Response(
                description="Incident not found",
                examples={"application/json": {"detail": "No UserIncident matches the given query."}}
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update a specific incident",
        operation_description="Update a specific incident using a given Incident ID",
        tags=["User Incidents"],
        responses={
            200: openapi.Response(
                description="Incident details after update.",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line",
                        "description": "Severe delays, platform overcrowded",
                        "severity": 4,
                        "created_at": "2026-03-12T17:30:00Z"
                    }
                }
            ), 
            400: openapi.Response(
                description="Error: Bad Request (Invalid input data - full request body required)",
                examples={
                    "application/json": {
                        "stop": [
                            "Stop ID is required."
                        ]
                    }
                }
            ),
            404: openapi.Response(
                description="Incident not found",
                examples={"application/json": {"detail": "No UserIncident matches the given query."}}
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update a specific incident",
        operation_description="Partially update a specific incident using a given Incident ID. Only the updated fields need to be provided in the request body.",
        tags=["User Incidents"],
        responses={
            200: openapi.Response(
                description="Incident details after partial update.",
                examples={
                    "application/json": {
                        "id": 1,
                        "user": "John Doe",
                        "stop": "Whitechapel (HUBZWL)",
                        "line": "Elizabeth line",
                        "description": "Severe delays, platform overcrowded",
                        "severity": 4,
                        "created_at": "2026-03-12T17:30:00Z"
                    }
                }
            ), 
            404: openapi.Response(
                description="Incident not found",
                examples={"application/json": {"detail": "No UserIncident matches the given query."}}
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a specific incident",
        operation_description="Delete a specific incident via a given Incident ID",
        tags=["User Incidents"],
        responses={
            204: openapi.Response(
                description="Incident deleted successfully",
            ), 
            404: openapi.Response(
                description="Incident not found",
                examples={"application/json": {"detail": "No UserIncident matches the given query."}}
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

### STOPS - Retrieving all stops based on mode
stop_list_example = [
    {
        "stop_id": "HUBBDS",
        "name": "Bond Street",
        "mode": "elizabeth-line",
        "lat": 51.513362,
        "lon": -0.148795
    },
    {
        "stop_id": "HUBCAW",
        "name": "Canary Wharf",
        "mode": "elizabeth-line",
        "lat": 51.503734,
        "lon": -0.019121
    },
    {
        "stop_id": "HUBEAL",
        "name": "Ealing Broadway",
        "mode": "elizabeth-line",
        "lat": 51.514993,
        "lon": -0.302131
    }
]

class StopListView(generics.ListAPIView):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["mode"]
    @swagger_auto_schema(
        operation_summary="Retrieve all stops in the database",
        operation_description="Retrieve all stops in the database. Supports filtering by mode (e.g. tube, elizabeth-line, dlr, overground, tram).",
        tags=["Stops"],
        responses={
            200: openapi.Response(
                description="List of stops as per filter. (Example filter: \"elizabeth-line\")",
                examples={"application/json": stop_list_example}
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# STOPS - Retrieving stop information with a given stop ID
stop_detail_example = {
    "stop_id": "HUBBDS",
    "name": "Bond Street",
    "mode": "elizabeth-line",
    "lat": 51.513362,
    "lon": -0.148795
}

class StopDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve a stop by ID",
        operation_description=(
            "Retrieve detailed information about a specific stop using its stop ID. "
            "Returns name, mode, and coordinates. "
            "Useful for validating stop IDs or displaying stop metadata."
        ),
        tags=["Stops"],
        responses={
            200: openapi.Response(
                description="Stop found",
                examples={"application/json": stop_detail_example}
            ),
            404: openapi.Response(
                description="Stop not found",
                examples={"application/json": {"error": "Stop ID not found"}}
            )
        }
    )
    def get(self, request, stop_id):
        try:
            stop = Stop.objects.get(stop_id=stop_id)
        except Stop.DoesNotExist:
            return Response(
                {"error": "Stop ID not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = StopSerializer(stop)
        return Response(serializer.data, status=200)

# LINES - Retrieving all lines in the database
line_list_example = [
    {
    "line_id": "bakerloo",
    "name": "Bakerloo",
    "mode": "tube"
    },
    {
    "line_id": "central",
    "name": "Central",
    "mode": "tube"
    },
    {
    "line_id": "circle",
    "name": "Circle",
    "mode": "tube"
    }
]

class LineListView(generics.ListAPIView):
    queryset = Line.objects.all()
    serializer_class = LineSerializer
    @swagger_auto_schema(
        operation_summary="Retrieve all lines in the database",
        operation_description="Retrieve all lines in the database.",
        tags=["Lines"],
        responses={
            200: openapi.Response(
                description="List of lines",
                examples={"application/json": line_list_example}
            )
        }
    )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# Arrivals
arrivals_example = [
  {
    "id": 2627,
    "direction": "outbound",
    "destination_name": "Hainault Underground Station",
    "predicted_time": "2026-03-12T18:11:37Z",
    "time_to_station": 1611,
    "recorded_at": "2026-03-12T17:44:54.319715Z",
    "stop": "940GZZLUNBP",
    "line": "central"
  },
  {
    "id": 2628,
    "direction": "outbound",
    "destination_name": "Hainault Underground Station",
    "predicted_time": "2026-03-12T17:45:38Z",
    "time_to_station": 52,
    "recorded_at": "2026-03-12T17:44:54.323132Z",
    "stop": "940GZZLUNBP",
    "line": "central"
  },
  {"...": "..."}
]

class StopArrivalsView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve arrival predictions for a stop",
        operation_description="Retrieves all previously saved arrival predictions for a stop. Use refresh = true to fetch and additionally return fresh data from TfL.",
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
            ),
            400: openapi.Response(
                description="Error: Bad Request - Invalid Stop ID",
                examples={"application/json": {"error": "Invalid Stop ID"}}
            )
        }
    )
    def get(self, request, stop_id):
        refresh_param = request.GET.get("refresh", "").lower()
        refresh = refresh_param in ["true", "1", "yes"]
        
        # Validate stop exists
        if not Stop.objects.filter(stop_id=stop_id).exists():
            return Response(
                {"error": "Invalid stop ID"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if refresh:
            arrivals = get_arrivals_for_stop(stop_id)
            for item in arrivals:
                data = transform_arrival(item)
                save_arrival(data)

        records = ArrivalRecord.objects.filter(stop_id=stop_id)
        serializer = ArrivalRecordSerializer(records, many=True)
        return Response(serializer.data)