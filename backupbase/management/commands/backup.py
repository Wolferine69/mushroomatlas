import os
from django.core.management.base import BaseCommand
from django.core import management
from datetime import datetime


class Command(BaseCommand):
    help = 'Backup the database into a JSON file'

    def handle(self, *args, **kwargs):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = 'backups'
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        output_file = os.path.join(backup_dir, f'backup_{timestamp}.json')

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                management.call_command('dumpdata', '--indent', '2', stdout=f)
            self.stdout.write(self.style.SUCCESS(f'Successfully backed up database to {output_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error backing up database: {e}'))

