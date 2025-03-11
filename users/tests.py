from django.test import TestCase
from users.models import CustomUser

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email="test@example.com", password="testpass")

    def test_create_user(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpass"))

    def test_create_superuser(self):
        admin_user = CustomUser.objects.create_superuser(email="admin@example.com", password="adminpass")
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
