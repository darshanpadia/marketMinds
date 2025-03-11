from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from dashboard.models import Asset, PredictedData
from datetime import datetime

class AssetDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )
        self.asset = Asset.objects.create(name="Bitcoin", symbol="BTC",open_price=0.0, close_price=0.0, volume=0.0, high=0.0, low=0.0,price_change=0.0,percent_change=0.0)

    def test_asset_detail_view(self):
        # Log in the user and confirm login success
        login_successful = self.client.login(email="testuser@example.com", password="testpassword")
        self.assertTrue(login_successful, "Test user login failed")

        # Fetch the asset detail page
        url = reverse("dashboard:individual-asset", kwargs={"symbol": self.asset.symbol})
        response = self.client.get(url)

        # Debugging: Print response status and possible redirect URL
        print(f"Response status: {response.status_code}")
        if response.status_code == 302:
            print(f"Redirect URL: {response.url}")

        # Assert correct page load
        self.assertEqual(response.status_code, 200, f"Unexpected response code: {response.status_code}")
        self.assertContains(response, "Bitcoin")


    def test_add_prediction(self):
        prediction = PredictedData.objects.create(
        asset=self.asset,
        date=datetime.now(),
        predicted_price=45000.0,
        predicted_high=45500.0,
        predicted_low=44500.0,
        predicted_open_price=44800.0,
        timeframe="day",
        confidence=0.85, 
        duration=1,
    )
        self.assertEqual(prediction.asset.symbol, "BTC")
        self.assertEqual(prediction.timeframe, "day")
        self.assertEqual(prediction.predicted_price, 45000)
