from rest_framework.response import Response
from rest_framework.views import APIView

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

class StopAverageWaitView(APIView):
    def get(self, request, stop_id):
        avg = average_wait_for_stop(stop_id)
        data = {"stop_id": stop_id, "average_wait_seconds": avg}
        return Response(AverageWaitSerializer(data).data)

class LineHeadwayView(APIView):
    def get(self, request, line_id):
        headway = average_headway_for_line(line_id)
        data = {"line_id": line_id, "average_headway_seconds": headway}
        return Response(LineHeadwaySerializer(data).data)

class LineStatusView(APIView):
    def get(self, request, line_id):
        status, wait = line_status(line_id)
        data = {
            "line_id": line_id,
            "status": status,
            "average_wait_seconds": wait
        }
        return Response(LineStatusSerializer(data).data)
