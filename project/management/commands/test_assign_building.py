from django.core.management.base import BaseCommand
from project.models import Building
from project.views import assign_building  # Adjust import based on where assign_building is located

class Command(BaseCommand):
    help = 'Test the assign_building function'

    def handle(self, *args, **options):
        result = assign_building('junior_staff', 30)
        print(result)