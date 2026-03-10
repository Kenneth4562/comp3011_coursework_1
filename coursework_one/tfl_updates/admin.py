from django.contrib import admin
from .models import Stop, Line, UserRoute, UserStation, ArrivalRecord, UserIncident

# Register your models here.
admin.site.register(Stop)
admin.site.register(Line)
admin.site.register(UserRoute)
admin.site.register(UserStation)
admin.site.register(ArrivalRecord)
admin.site.register(UserIncident)