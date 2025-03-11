from django.core.management.base import BaseCommand
from django.contrib import messages
from django.contrib.admin.utils import model_ngettext
from dashboard.models import Asset
from dashboard.admin import AssetAdmin

class Command(BaseCommand):
    help = "Updates historical data and predictions for all assets in the database."

    def handle(self, *args, **options):
        # Get all assets
        assets = Asset.objects.all()
        asset_admin = AssetAdmin(model=Asset, admin_site=None)

        # Call the update_historical_and_predictions action
        updated_count = 0
        failed_assets = []

        for asset in assets:
            try:
                # Call the action for each asset
                asset_admin.update_historical_and_predictions(None, Asset.objects.filter(id=asset.id))
                updated_count += 1
            except Exception as e:
                failed_assets.append(f"{asset.symbol}: {e}")

        # Output results
        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated {updated_count} asset(s).")
        )
        if failed_assets:
            self.stdout.write(
                self.style.ERROR(f"Failed to update: {', '.join(failed_assets)}")
            )