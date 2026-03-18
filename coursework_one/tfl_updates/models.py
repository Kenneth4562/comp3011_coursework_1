from django.db import models
from django.contrib.auth.models import User

class Stop(models.Model):
    stop_id = models.CharField(max_length=50, primary_key=True)  # NaPTAN ID
    name = models.CharField(max_length=200)
    mode = models.CharField(max_length=50)  # dlr, tube, tram
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.stop_id})"
    
class Line(models.Model):
    line_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    mode = models.CharField(max_length=50)  # dlr, tube, tram

    def __str__(self):
        return self.name

class UserRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name="routes_from")
    to_stop = models.ForeignKey(Stop, on_delete=models.CASCADE, related_name="routes_to")
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class UserStation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class ArrivalRecord(models.Model):
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)
    direction = models.CharField(max_length=50, null=True, blank=True)
    destination_name = models.CharField(max_length=200, null=True, blank=True)
    predicted_time = models.DateTimeField()
    time_to_station = models.IntegerField(null=True, blank=True)  # TfL gives this
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.line} at {self.stop}"

class UserIncident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stop = models.ForeignKey(Stop, on_delete=models.CASCADE)
    line = models.ForeignKey(Line, on_delete=models.CASCADE)

    description = models.TextField()
    severity = models.IntegerField(default=1)  # 1–5 scale
    created_at = models.DateTimeField(auto_now_add=True)