from datetime import datetime

def transform_arrival(item):
    return {
        "line_id": item["lineId"],
        "stop_id": item["naptanId"],
        "direction": item.get("direction"),
        "destination_name": item.get("destinationName"),
        "predicted_time": datetime.fromisoformat(item["expectedArrival"].replace("Z", "+00:00")),
        "time_to_station": item.get("timeToStation"),
    }
