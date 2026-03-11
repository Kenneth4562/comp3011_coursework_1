from django.core.management.base import BaseCommand
from tfl_updates.models import Stop
from tfl_updates.services.tfl_client import tfl_get

STOP_MODES = ["tube", "bus", "dlr", "overground", "tram"]  # add more if needed

class Command(BaseCommand):
    help = "Import all TfL stops into the database"

    def handle(self, *args, **options):
        for mode in STOP_MODES:
            self.stdout.write(self.style.NOTICE(f"Importing stops for mode: {mode}"))

            page = 1
            total_imported = 0

            while True:
                data = tfl_get(
                    f"StopPoint/Mode/{mode}",
                    params={"page": page, "pageSize": 500}  # TfL allows up to 500
                )

                stop_points = data.get("stopPoints", [])

                if not stop_points:
                    break  # No more pages

                for item in stop_points:
                    Stop.objects.update_or_create(
                        stop_id=item["id"],
                        defaults={
                            "name": item["commonName"],
                            "mode": mode,
                            "lat": item.get("lat"),
                            "lon": item.get("lon"),
                        }
                    )

                total_imported += len(stop_points)
                self.stdout.write(f"Page {page}: imported {len(stop_points)} stops")
                page += 1

            self.stdout.write(self.style.SUCCESS(
                f"Imported {total_imported} {mode} stops"
            ))
