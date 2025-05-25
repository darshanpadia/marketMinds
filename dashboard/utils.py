import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from .models import HistoricalData, PredictedData
import yfinance as yf
import logging

logger = logging.getLogger('celery')

def save_historical_data(asset):
    """Fetch and save historical data for the given asset."""
    try:
        logger.info(f"Fetching historical data for asset: {asset.symbol}")
        asset_data = yf.Ticker(asset.symbol)
        timeframes = {
            'day': asset_data.history(period='1d', interval='1h'),
            'week': asset_data.history(period='5d', interval='1d'),
            'month': asset_data.history(period='1mo', interval='1d'),
            'year': asset_data.history(period='1y', interval='1d'),
        }

        for timeframe, df in timeframes.items():
            if not df.empty:
                print(f"Processing {timeframe} data for asset: {asset.symbol}")
                df = df.reset_index()
                df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits']
                for _, row in df.iterrows():
                    HistoricalData.objects.create(
                        asset=asset,
                        date=row['Date'],
                        open_price=row['Open'],
                        close_price=row['Close'],
                        high=row['High'],
                        low=row['Low'],
                        volume=row['Volume'],
                        timeframe=timeframe,
                    )
                logger.info(f"Successfully saved {timeframe} data for asset: {asset.symbol}")
            else:
                logger.info(f"No data found for {timeframe} timeframe for asset: {asset.symbol}")    
    except Exception as e:
        logger.info(f"Error saving historical data for asset {asset.symbol}: {e}")
        raise Exception(f"Error saving historical data: {e}")

def predict_asset_prices(asset):
    try:
        logger.info(f"Starting price prediction for asset: {asset.symbol}")
        historical_data = HistoricalData.objects.filter(asset=asset).order_by('date')
        
        if historical_data.count() == 0:
            raise ValueError("No historical data found for the asset.")
        
        data = pd.DataFrame(list(historical_data.values('date','open_price', 'high', 'low', 'close_price')))
        data['date'] = pd.to_datetime(data['date'])
        data = data.groupby('date').agg({
            'open_price': 'mean',
            'high': 'mean',
            'low': 'mean',
            'close_price': 'mean',
        }).reset_index()

        data = data.sort_values('date').set_index('date')
        
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data[['open_price', 'high', 'low', 'close_price']])

        def create_sequences(data, time_steps=60):
            X, y = [], []
            for i in range(len(data) - time_steps):
                X.append(data[i:(i + time_steps), :])
                y.append(data[i + time_steps, :])
            return np.array(X), np.array(y)

        X, y = create_sequences(scaled_data, time_steps=60)
        X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2]))

        model = Sequential([
            Input(shape=(X.shape[1], X.shape[2])),
            LSTM(units=50, return_sequences=False),
            Dense(units=4)
        ])
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X, y, epochs=10, batch_size=32)

        def forecast_prices(time_steps):
            prediction_input = X[-1:]
            predictions = []
            for _ in range(time_steps):
                forecast = model.predict(prediction_input, verbose=0)
                predictions.append(forecast[0])
                prediction_input = np.append(prediction_input[:, 1:, :], forecast.reshape(1, 1, 4), axis=1)
            return scaler.inverse_transform(np.array(predictions))

        forecast_day = forecast_prices(24)
        forecast_week = forecast_prices(7)
        forecast_month = forecast_prices(30)
        forecast_year = forecast_prices(365)

        def save_predictions(forecast_values, timeframe):
            for i, (open_price, high, low, close_price) in enumerate(forecast_values):
                if timeframe == 'day':
                    predicted_date = data.index[-1] + timedelta(hours=i + 1)
                else:
                    predicted_date = data.index[-1] + timedelta(days=i + 1)

                duration = max(1, (predicted_date.date() - datetime.now().date()).days)
                confidence = max(0.5, 1 - abs(close_price - asset.close_price) / asset.close_price) * 100

                PredictedData.objects.create(
                    asset=asset,
                    date=predicted_date,
                    predicted_open_price=open_price,
                    predicted_high=high,
                    predicted_low=low,
                    predicted_price=close_price,
                    timeframe=timeframe,
                    confidence=confidence,
                    duration=duration,
                )

        save_predictions(forecast_day, 'day')
        save_predictions(forecast_week, 'week')
        save_predictions(forecast_month, 'month')
        save_predictions(forecast_year, 'year')

        logger.info(f"All predictions saved for asset {asset.symbol}")

    except Exception as e:
        logger.info(f"Error in predict_asset_prices: {e}")
        raise Exception(f"Error predicting prices: {e}")

def fetch_asset_data(asset):
    """Fetches latest asset data from Yahoo Finance and updates the asset instance."""
    symbol = asset.symbol
    try:
        # Fetch asset data
        asset_data = yf.Ticker(symbol)
        hist_day = asset_data.history(period='1d', interval='1h')

        if hist_day.empty:
            raise ValueError(f"Data for {symbol} could not be found.")

        # Populate asset fields with latest data
        latest_data = hist_day.iloc[-1]
        asset.name = asset_data.info.get('longName', symbol)
        asset.open_price = latest_data.get('Open', 0)
        asset.close_price = latest_data.get('Close', 0)
        asset.volume = latest_data.get('Volume', 0)
        asset.high = latest_data.get('High', 0)
        asset.low = latest_data.get('Low', 0)
        asset.price_change = latest_data.get('Close') - hist_day.iloc[-2].get('Close')
        asset.percent_change = (latest_data.get('Close') - hist_day.iloc[-2].get('Close')) / hist_day.iloc[-2].get('Close')

        return asset  # Return updated asset instance

    except Exception as e:
        raise ValueError(f"Error fetching data for {symbol}: {e}")
    
