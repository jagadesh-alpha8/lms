import csv
from django.core.management.base import BaseCommand
from std_qr.models import Zone, District, College


class Command(BaseCommand):

    help = "Import Zone, District, College from CSV"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):

        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8-sig') as f:

            reader = csv.DictReader(f)

            for row in reader:

                zone_name = row['Zone'].strip()
                district_name = row['District'].strip()
                college_name = row['College Name'].strip()

                # Zone
                zone, _ = Zone.objects.get_or_create(
                    name=zone_name
                )

                # District
                district, _ = District.objects.get_or_create(
                    name=district_name,
                    zone=zone
                )

                # College
                college, _ = College.objects.get_or_create(name=college_name,district=district)


                self.stdout.write(
                    self.style.SUCCESS(
                        f"Imported: {zone_name} > {district_name} > {college_name}"
                    )
                )

        self.stdout.write(self.style.SUCCESS("✅ Import Completed"))
