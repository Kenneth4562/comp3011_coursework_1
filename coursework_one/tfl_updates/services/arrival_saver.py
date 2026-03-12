from tfl_updates.models import ArrivalRecord, Stop, Line

def save_arrival(data):
    # Ensure Stop and Line exist
    stop, _ = Stop.objects.get_or_create(stop_id=data["stop_id"])
    line, _ = Line.objects.get_or_create(line_id=data["line_id"], defaults={"name": data["line_id"], "mode": "unknown"})

    ArrivalRecord.objects.create(
        stop=stop,
        line=line,
        direction=data["direction"],
        destination_name=data["destination_name"],
        predicted_time=data["predicted_time"],
        time_to_station=data["time_to_station"],
    )
