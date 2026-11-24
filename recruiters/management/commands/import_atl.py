import pandas as pd
from django.core.management.base import BaseCommand, CommandError
from recruiters.models import ActiveTaxpayer


class Command(BaseCommand):
    help = 'Import FBR Active Taxpayer List (Excel/CSV). Usage: manage.py import_atl path/to/file.xlsx'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to Excel or CSV file')

    def handle(self, *args, **opts):
        path = opts['path']
        try:
            if path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(path, dtype=str)
            else:
                df = pd.read_csv(path, dtype=str)
        except Exception as e:
            raise CommandError(f"Could not read file {path}: {e}")

        # IMPORTANT: column names depend on the file FBR currently publishes.
        # Detect NTN and Name columns case-insensitively and print what was used.
        cols = {str(c).lower().strip(): c for c in df.columns}
        try:
            ntn_col = next(c for k, c in cols.items() if 'ntn' in k)
        except StopIteration:
            raise CommandError("Could not find column containing 'ntn' in file header.")

        try:
            name_col = next(c for k, c in cols.items() if 'name' in k)
        except StopIteration:
            raise CommandError("Could not find column containing 'name' in file header.")

        rows = []
        for _, r in df.iterrows():
            val_ntn = str(r[ntn_col]).replace('-', '').strip()
            val_name = str(r[name_col]).strip()
            if val_ntn and val_ntn.lower() != 'nan':
                rows.append(ActiveTaxpayer(ntn=val_ntn, name=val_name))

        ActiveTaxpayer.objects.bulk_create(
            rows,
            batch_size=5000,
            update_conflicts=True,
            unique_fields=['ntn'],
            update_fields=['name']
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {len(rows)} rows using columns {ntn_col!r} and {name_col!r}'
            )
        )
