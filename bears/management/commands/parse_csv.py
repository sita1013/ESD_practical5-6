from django.core.management.base import BaseCommand
from bears.models import Bear, Sighting
import csv
from pathlib import Path

class Command(BaseCommand):
    help = 'Load data from CSV'

    def handle(self, *args, **options):
        Bear.objects.all().delete()
        print("Bear table cleared.")

        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        # Load Bears
        with open(base_dir / 'bears/bears_data/PolarBear_Telemetry_southernBeaufortSea_2009_2011/USGS_WC_eartag_deployments_2009-2011.csv', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for row in reader:
                bear = Bear.objects.create(
                    bearID=int(row[0]),
                    pTT_ID=int(row[1]),
                    capture_lat=float(row[6]),
                    capture_long=float(row[7]),
                    sex=row[9],
                    age_class=row[10],
                    ear_applied=row[11],
                )
                print(f"Created Bear {bear.bearID}")

        # Load Sightings
        with open(base_dir / 'bears/data/USGS_WC_eartags_output_files_2009-2011-Status.csv', newline='') as f:
            reader = csv.reader(f, delimiter=",")
            next(reader)
            for row in reader:
                if row[4] != '':
                    bear_temp = row[0]
                    try:
                        bear = Bear.objects.get(bearID=bear_temp)
                        sighting = Sighting.objects.create(
                            deploy_id=int(row[0]),
                            bear_id=bear,
                            recieved=row[2],
                            latitude=float(row[4]),
                            longitude=float(row[5]),
                            temperature=float(row[9]),
                        )
                        print(f"Created Sighting for Bear {bear.bearID}")
                    except Bear.DoesNotExist:
                        print(f"No Bear found with ID {bear_temp}")
                else:
                    continue

        print("Data parsed successfully.")
