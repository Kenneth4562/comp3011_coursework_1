from .arrival_saver import save_arrival
from .arrival_transformer import transform_arrival
from .tfl_client import get_arrivals_for_stop
from tfl_updates.models import ArrivalRecord
from django.db.models import Avg
from datetime import timedelta

def average_wait_for_stop(stop_id):
    arrivals = get_arrivals_for_stop(stop_id)
    currArrivalsTransformed = []
    for item in arrivals:
        data = transform_arrival(item)
        currArrivalsTransformed.append(data)
        save_arrival(data)

    shortestWait = []
    stopLines = []
    
    for arrival in currArrivalsTransformed:
        if arrival["line_id"] not in stopLines:
            stopLines.append(arrival["line_id"])
            shortestWait.append(arrival["time_to_station"])
        else:
            lineIndex = stopLines.index(arrival["line_id"])
            if arrival["time_to_station"] < shortestWait[lineIndex]:
                shortestWait[lineIndex] = arrival["time_to_station"]
    
    if not shortestWait:
        avg_wait = 0
    else:
        avg_wait = sum(shortestWait) / len(shortestWait)

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
