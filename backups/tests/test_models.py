from django.test import TestCase
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backup_service.settings')
django.setup()

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from backups.models import Backup


class BackupModelTest(TestCase):

    def test_create_backup(self):
        user = User.objects.create_user(username="test", password="123")
        file = SimpleUploadedFile("test.txt", b"hello world")

        backup = Backup.objects.create(
            user=user,
            name="backup1",
            file=file,
            size=123
        )

        self.assertEqual(backup.name, "backup1")
        self.assertEqual(backup.user.username, "test")
        self.assertTrue(backup.file.name.startswith("backups/"))