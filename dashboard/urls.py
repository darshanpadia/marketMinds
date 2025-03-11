from django.urls import path
from django.shortcuts import redirect
from .views import catalogue_view, add_to_watchlist_view,individual_asset, redirect_to_asset, search_assets, remove_from_watchlist_view

app_name = 'dashboard' #for using namespace argument

urlpatterns = [
    path('catalogue/', catalogue_view, name='catalogue'),
    path("", lambda request: redirect("home"), name="dashboard_home"),
    path('add_to_watchlist/<str:symbol>/', add_to_watchlist_view, name='add-to-watchlist'),
    path('asset/<str:symbol>/', individual_asset, name='individual-asset'),
    path('search/', search_assets, name='search_assets'),
    path('remove_from_watchlist/<str:symbol>/', remove_from_watchlist_view, name='remove-from-watchlist'),

]