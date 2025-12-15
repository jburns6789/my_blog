# my_blog/management/commands/restore_database.py
import os
import subprocess
import boto3
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Restore PostgreSQL database from S3 backup'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup_file',
            type=str,
            help='S3 backup filename to restore'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm database restoration (required)'
        )

    def handle(self, *args, **options):
        backup_file = options['backup_file']
        
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'WARNING: This will overwrite your current database!\n'
                    'Use --confirm flag to proceed.'
                )
            )
            return
        
        temp_dir = "/tmp"
        compressed_path = f"{temp_dir}/{backup_file}"
        decompressed_path = compressed_path.replace('.gz', '')
        
        try:
            # Step 1: Download from S3
            s3_client = boto3.client('s3')
            s3_bucket = 'myblog-backups'
            s3_key = f"database-backups/{backup_file}"
            
            self.stdout.write(f"Downloading from S3: {s3_key}")
            s3_client.download_file(s3_bucket, s3_key, compressed_path)
            
            # Step 2: Decompress
            self.stdout.write("Decompressing backup...")
            subprocess.run(['gunzip', compressed_path], check=True)
            
            # Step 3: Restore database
            db_config = settings.DATABASES['default']
            db_name = db_config['NAME']
            db_user = db_config['USER']
            db_password = db_config['PASSWORD']
            db_host = db_config['HOST']
            db_port = db_config.get('PORT', '5432')
            
            self.stdout.write(f"Restoring database: {db_name}")
            
            env = os.environ.copy()
            env['PGPASSWORD'] = db_password
            
            with open(decompressed_path, 'r') as backup_file:
                restore_cmd = [
                    'psql',
                    '-h', db_host,
                    '-p', str(db_port),
                    '-U', db_user,
                    '-d', db_name
                ]
                
                result = subprocess.run(
                    restore_cmd,
                    stdin=backup_file,
                    env=env,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode != 0:
                raise Exception(f"Restore failed: {result.stderr}")
            
            self.stdout.write(
                self.style.SUCCESS('✅ Database restored successfully!')
            )
            
            # Clean up
            if os.path.exists(decompressed_path):
                os.remove(decompressed_path)
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Restore failed: {str(e)}')
            )
            raise
