from django.contrib import admin
from django.contrib import messages
from .models import Asset, PredictedData, HistoricalData
from .forms import AssetAdminForm
import yfinance as yf
from .utils import fetch_asset_data, save_historical_data, predict_asset_prices
from .tasks import update_asset_data_task
from django.db import transaction

class AssetAdmin(admin.ModelAdmin):
    form = AssetAdminForm
    list_display = ('name', 'symbol', 'category', 'open_price', 'close_price', 'volume', 'high', 'low', 'predicted_price')
    actions = ['update_historical_and_predictions']

    def predicted_price(self, obj):
        """Display the most recent predicted price for the asset."""
        top_prediction = PredictedData.objects.filter(asset=obj).order_by('-confidence').first()
        return f"{top_prediction.predicted_price:.2f}" if top_prediction else "N/A"

    # def fetch_and_update_asset_data(self,object):
    #     """Fetches latest asset data from Yahoo Finance and updates the asset instance."""
    #     return fetch_asset_data(object)

    def save_model(self, request, obj, form, change):

        # If the only change is the 'image' field, save without updating other data
        if change and form.changed_data == ["image"]:
            super().save_model(request, obj, form, change)
            return

        """Save model after fetching latest data."""
        super().save_model(request, obj, form, change)
        # Save historical data and predictions
        update_asset_data_task.delay_on_commit(obj.symbol)
        messages.info(request,f"Background task started to fetch and update data for {obj.symbol}")

    # @admin.action(description="Update historical data and predictions")
    # def update_historical_and_predictions(self, request, queryset):
    #     """Deletes selected assets and recreates them with fresh data."""
    #     updated_count = 0
    #     failed_assets = []

    #     for asset in queryset:
    #         symbol = asset.symbol
    #         category = asset.category

    #         try:
    #             # Delete existing asset and related data
    #             asset.delete()

    #             # Create a new empty asset instance
    #             new_asset = Asset(symbol=symbol, category=category)

    #             # Fetch and update new asset data
    #             new_asset = self.fetch_and_update_asset_data(new_asset)
    #             new_asset.save()  # Save new asset

    #             # Save historical data and predictions
    #             form = AssetAdminForm(instance=new_asset)
    #             form.save_historical_data(new_asset)
    #             form.predict_asset_prices(new_asset)

    #             updated_count += 1

    #         except Exception as e:
    #             failed_assets.append(f"{symbol}: {e}")

    #     # Show success or error messages
    #     if updated_count:
    #         self.message_user(request, f"Successfully recreated {updated_count} asset(s).", messages.SUCCESS)
    #     if failed_assets:
    #         self.message_user(request, f"Failed to recreate: {', '.join(failed_assets)}", messages.ERROR)

admin.site.register(Asset, AssetAdmin)
