from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email="test@example.com", password="testpass")

    def test_home_view_status_code(self):
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)  # Check if home page is accessible

    def test_home_view_authenticated(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("home"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_view_requires_login(self):
        response = self.client.get(reverse("dashboard:dashboard_home"))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page

        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("dashboard:dashboard_home"), follow=True)  # Follow redirects
        self.assertEqual(response.status_code, 200)  # Should be accessible after login

