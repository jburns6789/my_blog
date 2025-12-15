import os
import subprocess
import boto3
from datetime import datetime
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backup PostgresSQL database naand upload to s3'

    def add_arguments(self, parser):
        parser.add_argument(
            '--prefix',
            type=str,
            default='manual',
            help='Backup filename prefix'
        )

    def handle(self, *args, **options):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = options['prefix']
        backup_filename = f"blog_backup_{prefix}_{timestamp}.sql"
        compressed_filename = f"{backup_filename}.gz"

        # Temp paths
        temp_dir = "/tmp"
        backup_path = f"{temp_dir}/{backup_filename}"
        compressed_path = f"{temp_dir}/{compressed_filename}"

        try:
            # Step 1: Get database credentials
            db_config = settings.DATABASES['default']
            db_name = db_config['NAME']
            db_user = db_config['USER']
            db_password = db_config['PASSWORD']
            db_host = db_config['HOST']
            db_port = db_config.get('PORT', '5432')
            
            self.stdout.write(f"Starting backup: {backup_filename}")
            
            # Step 2: Create database dump
            env = os.environ.copy()
            env['DATABASE_PASSWORD'] = db_password
            
            dump_cmd = [
                'pg_dump',
                '-h', db_host,
                '-p', str(db_port),
                '-U', db_user,
                '-d', db_name,
                '--no-owner',
                '--no-privileges',
                '-f', backup_path
            ]
            
            result = subprocess.run(
                dump_cmd,
                env=env,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
            
            # Verify backup file exists and has content
            if not os.path.exists(backup_path) or os.path.getsize(backup_path) == 0:
                raise Exception("Backup file is empty or was not created")
            
            file_size = os.path.getsize(backup_path)
            self.stdout.write(f"Database dump created: {file_size} bytes")
            
            # Step 3: Compress the backup
            compress_result = subprocess.run(
                ['gzip', backup_path],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if compress_result.returncode != 0:
                raise Exception(f"Compression failed: {compress_result.stderr}")
            
            compressed_size = os.path.getsize(compressed_path)
            self.stdout.write(f"Backup compressed: {compressed_size} bytes")
            
            # Step 4: Upload to S3
            s3_client = boto3.client('s3')
            s3_bucket = 'myblog-backups'
            s3_key = f"database-backups/{compressed_filename}"
            
            s3_client.upload_file(
                compressed_path,
                s3_bucket,
                s3_key,
                ExtraArgs={
                    'Metadata': {
                        'backup-date': timestamp,
                        'backup-type': prefix,
                        'database': db_name
                    },
                    'StorageClass': 'STANDARD_IA'  # Cost optimization
                }
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Backup successful: s3://{s3_bucket}/{s3_key}'
                )
            )
            
            # Step 5: Clean up local files
            if os.path.exists(compressed_path):
                os.remove(compressed_path)
                self.stdout.write("Local backup file cleaned up")
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Backup failed: {str(e)}')
            )
            raise

        return f"Backup completed: {compressed_filename}"