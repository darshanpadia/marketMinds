from celery import shared_task
from .models import Asset
import logging
from .utils import fetch_asset_data, save_historical_data, predict_asset_prices

logger = logging.getLogger('celery')

@shared_task
def update_asset_data_task(asset_symbol):
    try:
        asset = Asset.objects.get(symbol=asset_symbol)

        # Fetch latest asset data
        logger.info("Fetching asset details.")
        updated_asset = fetch_asset_data(asset)
        logger.info("Saving asset details..")
        updated_asset.save()

        # Save historical data and make predictions
        logger.info("Start saving historical data.")
        save_historical_data(updated_asset)
        logger.info("Start saving predictions.")
        predict_asset_prices(updated_asset)
        
        return f"Asset {asset.symbol} updated successfully."
    except Asset.DoesNotExist:
        return f"Asset with symbol {asset_symbol} not found."
    except Exception as e:
        return f"Error updating asset {asset_symbol}: {str(e)}"
    
