from django.urls import path
from .views import (
    UserRouteListCreateView, UserRouteDetailView,
    UserStationListCreateView, UserStationDetailView,
    UserIncidentListCreateView, UserIncidentDetailView,
    StopListView, LineListView
)
from .views_analytics import (
    StopAverageWaitView,
    LineHeadwayView,
    LineStatusView
)
from .views import StopArrivalsView

urlpatterns = [
    # User Routes
    path("routes/", UserRouteListCreateView.as_view(), name="route-list-create"),
    path("routes/<int:pk>/", UserRouteDetailView.as_view(), name="route-detail"),

    # User Stations
    path("stations/", UserStationListCreateView.as_view(), name="station-list-create"),
    path("stations/<int:pk>/", UserStationDetailView.as_view(), name="station-detail"),

    # User Incidents
    path("incidents/", UserIncidentListCreateView.as_view(), name="incident-list-create"),
    path("incidents/<int:pk>/", UserIncidentDetailView.as_view(), name="incident-detail"),
    
    path("stops/", StopListView.as_view(), name="stop-list"),
    path("lines/", LineListView.as_view(), name="line-list"),
    
    path("analytics/stops/<str:stop_id>/average-wait/", StopAverageWaitView.as_view()),
    path("analytics/lines/<str:line_id>/headway/", LineHeadwayView.as_view()),
    path("analytics/lines/<str:line_id>/status/", LineStatusView.as_view()),

    path("stops/<str:stop_id>/arrivals/", StopArrivalsView.as_view()),
]
