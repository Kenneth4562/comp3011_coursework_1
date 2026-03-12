from tfl_updates.models import ArrivalRecord
from django.db.models import Avg
from datetime import timedelta

def average_wait_for_stop(stop_id):
    avg_wait = ArrivalRecord.objects.filter(stop_id=stop_id).aggregate(
        avg=Avg("time_to_station")
    )["avg"]

    return avg_wait or 0

def average_headway_for_line(line_id):
    records = ArrivalRecord.objects.filter(line_id=line_id).order_by("predicted_time")

    if len(records) < 2:
        return None

    diffs = []
    for i in range(1, len(records)):
        delta = (records[i].predicted_time - records[i-1].predicted_time).total_seconds()
        if delta > 0:
            diffs.append(delta)

    return sum(diffs) / len(diffs) if diffs else None

def line_status(line_id):
    avg_wait = average_wait_for_stop  # reuse logic

    wait = ArrivalRecord.objects.filter(line_id=line_id).aggregate(
        avg=Avg("time_to_station")
    )["avg"]

    if wait is None:
        return "No data"

    if wait < 180:
        status = "Good service"
    elif wait < 600:
        status = "Minor delays"
    else:
        status = "Severe delays"

    return status, wait
