from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Deletes all migration files in all installed apps'

    def handle(self, *args, **options):
        apps = list(self.get_apps())
        
        for app in apps:
            self.delete_migrations(app)

    def get_apps(self):
        from django.apps import apps
        return apps.get_app_configs()

    def delete_migrations(self, app):
        migration_path = app.path + '/migrations'
        if os.path.exists(migration_path):
            migration_files = os.listdir(migration_path)
            migration_files = [f for f in migration_files if f.endswith('.py') and f != '__init__.py']
            
            if migration_files:
                for file_name in migration_files:
                    file_path = os.path.join(migration_path, file_name)
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'Deleted migration file: {file_name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'No migration files to delete in {app.label}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'No migrations directory found in {app.label}'))


