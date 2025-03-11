from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Asset(models.Model):
    ASSET_CATEGORIES = (
        ('stock', 'Stock'),
        ('crypto', 'Crypto'),
    )                                                                                                                                                                               
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=10,choices=ASSET_CATEGORIES)
    open_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    price_change = models.FloatField()
    percent_change = models.FloatField()
    image = models.ImageField(upload_to='asset_images/', default="asset_images/blank-product.jpg")


    def __str__(self):
        return f"{self.name} ({self.get_category_display()})" # self.category will return stock while this will rerturn Stock


class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlists")
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'asset')  # Ensures one asset can only be added once per user

    def __str__(self):
        return f"{self.user.email}'s Watchlist: {self.asset.name}"


class HistoricalData(models.Model):
    TIMEFRAME_CHOICES = [
        ('day', '1 Day'),
        ('week', '7 Days'),
        ('month', '1 Month'),
        ('year', '1 Year'),
    ]
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='historical_data_related')
    date = models.DateTimeField()
    close_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    open_price = models.FloatField()
    volume = models.BigIntegerField()
    timeframe = models.CharField(max_length=10, choices=TIMEFRAME_CHOICES)

    def __str__(self):
        return f'{self.asset.symbol} - {self.date}'


class PredictedData(models.Model):
    TIMEFRAME_CHOICES = [
        ('day', '1 Day'),
        ('week', '7 Days'),
        ('month', '1 Month'),
        ('year', '1 Year'),
    ]
    asset = models.ForeignKey("Asset", on_delete=models.CASCADE, related_name="predicted_data_related")
    date = models.DateTimeField()
    predicted_price = models.FloatField()
    predicted_high = models.FloatField()
    predicted_low = models.FloatField()
    predicted_open_price = models.FloatField()
    timeframe = models.CharField(max_length=10, choices=TIMEFRAME_CHOICES)
    confidence = models.FloatField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.asset.symbol} Prediction for {self.date}: {self.predicted_price} (Confidence: {self.confidence:.2f})"



