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