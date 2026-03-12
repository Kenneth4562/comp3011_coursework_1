from django.core.management.base import BaseCommand
from tfl_updates.models import Line
from tfl_updates.services.tfl_client import tfl_get

LINE_MODES = ["tube", "dlr", "overground", "elizabeth-line", "tram"]  # add more if needed

class Command(BaseCommand):
    help = "Import all TfL lines into the database"

    def handle(self, *args, **options):
        for mode in LINE_MODES:
            self.stdout.write(self.style.NOTICE(f"Importing lines for mode: {mode}"))

            data = tfl_get(f"Line/Mode/{mode}")

            for item in data:
                Line.objects.update_or_create(
                    line_id=item["id"],
                    defaults={
                        "name": item["name"],
                        "mode": mode,
                    }
                )

            self.stdout.write(self.style.SUCCESS(f"Imported {len(data)} {mode} lines"))
