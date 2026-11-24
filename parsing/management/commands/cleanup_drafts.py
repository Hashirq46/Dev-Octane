from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from parsing.models import ParsedDraft


class Command(BaseCommand):
    help = 'Deletes unsubmitted drafts and files older than 14 days'

    def handle(self, *args, **opts):
        cutoff = timezone.now() - timedelta(days=14)
        count = 0
        for d in ParsedDraft.objects.exclude(state='submitted').filter(created_at__lt=cutoff):
            if d.file:
                d.file.delete(save=False)
            d.delete()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} expired unsubmitted drafts.'))
