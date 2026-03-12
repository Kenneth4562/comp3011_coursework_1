from django.core.management.base import BaseCommand
from tfl_updates.models import Stop
from tfl_updates.services.tfl_client import get_arrivals_for_stop
from tfl_updates.services.arrival_transformer import transform_arrival
from tfl_updates.services.arrival_saver import save_arrival

class Command(BaseCommand):
    help = "Fetch real-time arrivals for all stops and store them"

    def handle(self, *args, **options):
        stops = Stop.objects.all()

        for stop in stops:
            self.stdout.write(f"Fetching arrivals for stop {stop.stop_id} ({stop.name})")

            try:
                arrivals = get_arrivals_for_stop(stop.stop_id)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching stop {stop.stop_id}: {e}"))
                continue

            for item in arrivals:
                data = transform_arrival(item)
                save_arrival(data)

        self.stdout.write(self.style.SUCCESS("Arrivals import complete"))
