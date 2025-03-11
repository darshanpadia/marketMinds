import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Input
from .models import HistoricalData, PredictedData
from .models import Watchlist
from django import forms
from .models import Asset
from statsmodels.tsa.arima.model import ARIMA
from datetime import timedelta
import yfinance as yf

class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['asset'] 

class AssetAdminForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = ['symbol', 'category', 'image']

    def clean(self):
        """Perform validation for uploaded files and the symbol field."""
        cleaned_data = super().clean()
        symbol = cleaned_data.get('symbol')
        # predicted_data_file = cleaned_data.get('predicted_data')

        # Validate the symbol field
        if not symbol:
            print("Symbol is required.")
            raise forms.ValidationError("Symbol is required.")

    def save_historical_data(self, asset):
        """Fetch and save historical data for the given asset."""
        try:
            print(f"Fetching historical data for asset: {asset.symbol}")
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
                    print(f"Successfully saved {timeframe} data for asset: {asset.symbol}")
                else:
                    print(f"No data found for {timeframe} timeframe for asset: {asset.symbol}")    
        except Exception as e:
            print(f"Error saving historical data for asset {asset.symbol}: {e}")
            raise forms.ValidationError(f"Error saving historical data: {e}")


    def predict_asset_prices(self, asset):
        try:
            # Fetch historical data for the asset
            print(f"Starting price prediction for asset: {asset.symbol}")
            historical_data = HistoricalData.objects.filter(asset=asset).order_by('date')
            
            if historical_data.count() == 0:
                print(f"No historical data found for asset: {asset.symbol}")
                raise ValueError("No historical data found for the asset.")
            
            # Convert the historical data into a pandas DataFrame
            data = pd.DataFrame(list(historical_data.values('date','open_price', 'high', 'low', 'close_price')))
            print(f"Historical data fetched and converted to DataFrame for asset: {asset.symbol}")
            
            # Handle duplicates in the date column by grouping and averaging the prices
            data['date'] = pd.to_datetime(data['date'])
            data = data.groupby('date').agg({
                'open_price': 'mean',
                'high': 'mean',
                'low': 'mean',
                'close_price': 'mean',
            }).reset_index()
            print("Duplicates in date column handled by grouping and averaging.")

            # Prepare the data for LSTM model
            data = data.sort_values('date')
            data = data.set_index('date')
            print("Data sorted and indexed by date.")
            
            # Normalize the data using MinMaxScaler
            scaler = MinMaxScaler(feature_range=(0, 1))
            scaled_data = scaler.fit_transform(data[['open_price', 'high', 'low', 'close_price']])
            print("Data normalized using MinMaxScaler.")

            # Create data sequences for LSTM
            def create_sequences(data, time_steps=60):
                X, y = [], []
                for i in range(len(data) - time_steps):
                    X.append(data[i:(i + time_steps), :])  # Features: past 'time_steps' prices
                    y.append(data[i + time_steps, :])      # Target: next price after 'time_steps'
                return np.array(X), np.array(y)

            # Prepare training data
            X, y = create_sequences(scaled_data, time_steps=60)
            X = np.reshape(X, (X.shape[0], X.shape[1], X.shape[2]))  # Reshape for LSTM input (samples, time_steps, features)
            print("Training data prepared for LSTM model.")

            # Build LSTM model
            model = Sequential([
                Input(shape=(X.shape[1], X.shape[2])),
                LSTM(units=50, return_sequences=False),
                Dense(units=4)
            ])
            model.compile(optimizer='adam', loss='mean_squared_error')
            print("LSTM model built and compiled.")

            # Train the model
            model.fit(X, y, epochs=10, batch_size=32)
            print("LSTM model training completed.")

            def forecast_prices(time_steps):
                prediction_input = X[-1:]  # Start with the last known sequence
                predictions = []

                for _ in range(time_steps):
                    forecast = model.predict(prediction_input)  # Predict next step
                    predictions.append(forecast[0])  # Store prediction

                    # Append the new prediction to the input and remove the oldest value
                    prediction_input = np.append(prediction_input[:, 1:, :], forecast.reshape(1, 1, 4), axis=1)

                predictions = np.array(predictions)
                return scaler.inverse_transform(predictions)  # Convert back to original scale
            

            forecast_day = forecast_prices(24)  # 1-day forecast (hourly)
            forecast_week = forecast_prices(7)  # 7-day forecast (daily)
            forecast_month = forecast_prices(30)  # 1-month forecast (daily)
            forecast_year = forecast_prices(365)  # 1-year forecast (daily)
            print("Forecasting completed for all timeframes.")

            # Function to save predictions
            def save_predictions(forecast_values, timeframe):
                for i, (open_price, high, low, close_price) in enumerate(forecast_values):
                    if timeframe == 'day':
                        predicted_date = data.index[-1] + timedelta(hours=i + 1)  # Increment time correctly
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

            # Save predictions for each timeframe
            print("Saving predictions into database...")
            save_predictions(forecast_day, 'day')
            save_predictions(forecast_week, 'week')
            save_predictions(forecast_month, 'month')
            save_predictions(forecast_year, 'year')
            print("All predictions saved successfully.")

        except Exception as e:
            print(f"Error in predict_asset_prices: {e}")
            raise forms.ValidationError(f"Error predicting prices: {e}")

        