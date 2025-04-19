from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Asset, Watchlist, PredictedData, HistoricalData
from .forms import WatchlistForm

from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def add_to_watchlist_view(request, symbol):
    """Adds an asset to the user's watchlist via a standard form submission."""
    if request.method == "POST":
        try:
            asset = Asset.objects.get(symbol=symbol)
            user = request.user

            if Watchlist.objects.filter(user=user, asset=asset).exists():
                messages.warning(request, "Already in watchlist")
            else:
                Watchlist.objects.create(user=user, asset=asset)
                messages.success(request, "Added to watchlist")

            return redirect(request.META.get('HTTP_REFERER', 'dashboard:home'))  # Redirects back to the page
        except Asset.DoesNotExist:
            messages.error(request, "Asset not found")
            return redirect('dashboard:home')

    messages.error(request, "Invalid request")
    return redirect('dashboard:home')

@login_required
@csrf_exempt  # For AJAX POST requests
def remove_from_watchlist_view(request, symbol):
    """Removes an asset from the user's watchlist via AJAX."""
    if request.method == "POST":
        try:
            asset = Asset.objects.get(symbol=symbol)
            user = request.user

            # Check if asset is in watchlist
            watchlist_entry = Watchlist.objects.filter(user=user, asset=asset)
            if watchlist_entry.exists():
                watchlist_entry.delete()
                return JsonResponse({"message": "Removed from watchlist"}, status=200)
            else:
                return JsonResponse({"message": "Not in watchlist"}, status=400)
        except Asset.DoesNotExist:
            return JsonResponse({"message": "Asset not found"}, status=404)
    return JsonResponse({"message": "Invalid request"}, status=400)



@login_required
def home_view(request):
    # Get the user's watchlist
    user_watchlist = Watchlist.objects.filter(user=request.user)

    # Separate the assets into stocks and cryptos based on the watchlist
    user_stocks = Asset.objects.filter(id__in=user_watchlist.filter(asset__category='stock').values('asset'))
    user_cryptos = Asset.objects.filter(id__in=user_watchlist.filter(asset__category='crypto').values('asset'))

    # Fetch the top predictions for each asset
    stocks_with_top_predictions = []
    cryptos_with_top_predictions = []

    # Get the top prediction for each stock
    for stock in user_stocks:
        top_prediction = PredictedData.objects.filter(asset=stock).order_by('-confidence').first()
        stocks_with_top_predictions.append({
            'asset': stock,
            'top_prediction': top_prediction
        })

    # Get the top prediction for each crypto
    for crypto in user_cryptos:
        top_prediction = PredictedData.objects.filter(asset=crypto).order_by('-confidence').first()
        cryptos_with_top_predictions.append({
            'asset': crypto,
            'top_prediction': top_prediction
        })

    return render(request, 'home.html', {
        'stocks': stocks_with_top_predictions,
        'cryptos': cryptos_with_top_predictions,
    })

@login_required
def catalogue_view(request):
    stocks = Asset.objects.filter(category='stock')
    cryptos = Asset.objects.filter(category='crypto')

    # Check if user is authenticated to display their watchlist status
    if request.user.is_authenticated:
        user_watchlist = Watchlist.objects.filter(user=request.user).values_list('asset', flat=True)

    return render(request, 'dashboard/catalogue.html', {
        'stocks': stocks,
        'cryptos': cryptos,
        'user_watchlist': user_watchlist,  # This will hold the IDs of the user's watchlist assets
    })

@login_required
def individual_asset(request, symbol):
    # Fetch the asset object using its symbol
    asset = get_object_or_404(Asset, symbol=symbol)

    # Fetch the historical data and forecasts for the asset
    hist_day = HistoricalData.objects.filter(asset=asset, timeframe='day').order_by('-date')
    hist_week = HistoricalData.objects.filter(asset=asset, timeframe='week').order_by('-date')
    hist_month = HistoricalData.objects.filter(asset=asset, timeframe='month').order_by('-date')
    hist_year = HistoricalData.objects.filter(asset=asset, timeframe='year').order_by('-date')

    # Fetch the forecasts
    pred_day = PredictedData.objects.filter(asset=asset, timeframe='day').order_by('date')
    pred_week = PredictedData.objects.filter(asset=asset, timeframe='week').order_by('date')
    pred_month = PredictedData.objects.filter(asset=asset, timeframe='month').order_by('date')
    pred_year = PredictedData.objects.filter(asset=asset, timeframe='year').order_by('date')

    def get_trends(hist_data):
        # Prepare a new list with comparison flags
        enhanced_data = []

        for i in range(len(hist_data)):
            row = hist_data[i]
            prev = hist_data[i + 1] if i + 1 < len(hist_data) else None
            enhanced_data.append({
                'date': row.date,
                'open_price': row.open_price,
                'close_price': row.close_price,
                'high': row.high,
                'low': row.low,
                'open_trend' : 'up' if prev and row.open_price > prev.open_price else 'down' if prev else 'neutral',
                'close_trend': 'up' if prev and row.close_price > prev.close_price else 'down' if prev else 'neutral',
                'high_trend': 'up' if prev and row.high > prev.high else 'down' if prev else 'neutral',
                'low_trend': 'up' if prev and row.low > prev.low else 'down' if prev else 'neutral',
            })
        return enhanced_data
    
    def get_pred_trends(pred_data):
        # Prepare a new list with comparison flags
        enhanced_data = []

        for i in range(len(pred_data)):
            row = pred_data[i]
            prev = pred_data[i - 1] if i > 0 else None
            enhanced_data.append({
                'date': row.date,
                'open_price': row.predicted_open_price,
                'close_price': row.predicted_price,
                'high': row.predicted_high,
                'low': row.predicted_low,
                'open_trend' : 'up' if prev and row.predicted_open_price > prev.predicted_open_price else 'down' if prev else 'neutral',
                'close_trend': 'up' if prev and row.predicted_price > prev.predicted_price else 'down' if prev else 'neutral',
                'high_trend': 'up' if prev and row.predicted_high > prev.predicted_high else 'down' if prev else 'neutral',
                'low_trend': 'up' if prev and row.predicted_low > prev.predicted_low else 'down' if prev else 'neutral',
            })
        return enhanced_data

    # for asset in hist_day:
    #     print(asset)
    # for asset in hist_week:
    #     print('w')
    #     print(asset)

    context = {
        'asset': asset,
        'hist_day': get_trends(hist_day),
        'hist_week' : get_trends(hist_week),
        'hist_month' : get_trends(hist_month),
        'hist_year' : get_trends(hist_year),
        'pred_day': get_pred_trends(pred_day),
        'pred_week' : get_pred_trends(pred_week),
        'pred_month' : get_pred_trends(pred_month),
        'pred_year' : get_pred_trends(pred_year),

    }
    return render(request, 'dashboard/asset.html', context)

def search_assets(request):
    """Handles AJAX search for assets."""
    query = request.GET.get('q', '')

    if len(query) < 3:
        return JsonResponse({'results': []})  # Avoid unnecessary queries

    assets = Asset.objects.filter(name__icontains=query)[:10]  # Limit results
    results = [{'name': asset.name, 'symbol': asset.symbol, 'id': asset.id} for asset in assets]

    return JsonResponse({'results': results})


def redirect_to_asset(request, symbol):
    """Redirect to the individual asset page when an asset is clicked."""
    asset = get_object_or_404(Asset, symbol=symbol)
    return redirect('individual-asset', symbol=asset.symbol)  # Ensure 'asset_detail' is your asset page URL name
