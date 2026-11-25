from django.core.management.base import BaseCommand
from django.utils import timezone
from scholarships.models import Scholarship
from scholarships.views.utils import auto_cleanup_expired_scholarships


class Command(BaseCommand):
    help = 'Automatically cleans up or permanently deletes expired scholarships'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force-delete-all',
            action='store_true',
            help='Permanently delete ALL expired scholarships regardless of applications',
        )

    def handle(self, *args, **options):
        today = timezone.now().date()
        force_delete = options.get('force_delete_all', False)

        if force_delete:
            deleted_count = auto_cleanup_expired_scholarships(purge=True)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully deleted {deleted_count} expired scholarships.')
            )
        else:
            # 1. Delete expired scholarships with 0 applications
            del_count, _ = Scholarship.objects.filter(
                end_date__lt=today, applications__isnull=True
            ).delete()
            # 2. Close remaining expired scholarships with applications
            closed_count = Scholarship.objects.filter(
                end_date__lt=today, status='active'
            ).update(status='closed')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Cleanup complete: deleted {del_count} expired scholarship(s) with no apps, '
                    f'closed {closed_count} expired scholarship(s) with apps.'
                )
            )
