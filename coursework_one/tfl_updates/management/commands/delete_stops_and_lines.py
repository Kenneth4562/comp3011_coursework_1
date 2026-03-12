from django.core.management.base import BaseCommand
from tfl_updates.models import Stop, Line

class Command(BaseCommand):
    help = "Deletes all records from the Stop table."

    def handle(self, *args, **options):
        count, _ = Stop.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} records from Stop."))
        count, _ = Line.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {count} records from Line."))
