from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from backups.models import Backup


class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test",
            password="123"
        )
        self.client.login(username="test", password="123")

    def test_dashboard_get(self):
        response = self.client.get("/backups/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        self.client.logout()
        response = self.client.get("/backups/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_upload_backup(self):
        file = SimpleUploadedFile("file.txt", b"hello")

        response = self.client.post("/backups/dashboard/", {
            "name": "backup1",
            "file": file
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Backup.objects.count(), 1)

    def test_upload_without_file(self):
        response = self.client.post("/backups/dashboard/", {
            "name": "no file"
        })

        self.assertEqual(Backup.objects.count(), 0)

    def test_upload_without_name(self):
        file = SimpleUploadedFile("file.txt", b"hello")

        response = self.client.post("/backups/dashboard/", {
            "file": file
        })

        self.assertEqual(Backup.objects.count(), 0)

    def test_delete_backup(self):
        file = SimpleUploadedFile("file.txt", b"hello")

        backup = Backup.objects.create(
            user=self.user,
            name="test",
            file=file,
            size=10
        )

        response = self.client.post(f"/backups/delete/{backup.id}/")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Backup.objects.count(), 0)

    def test_cannot_delete_other_user_backup(self):
        other_user = User.objects.create_user(
            username="other",
            password="123"
        )

        file = SimpleUploadedFile("file.txt", b"hello")

        backup = Backup.objects.create(
            user=other_user,
            name="other",
            file=file,
            size=10
        )

        response = self.client.post(f"/backups/delete/{backup.id}/")

        self.assertEqual(Backup.objects.count(), 1)