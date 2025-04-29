📈 MarketMinds – Smart Asset Monitoring & Prediction System

MarketMinds is a full-stack Django web application designed for tracking and predicting stock and cryptocurrency trends. It offers features like watchlist management, AI-based forecasting, live tracking, a responsive catalogue, and a personalized dashboard.

🚀 Features Overview

🔹 Dashboard

Displays categorized assets: Stocks and Cryptos.

Tabbed layout with active tab persistence across actions (like adding to watchlist).

Highlights best predictions for each asset.

Quick access to watchlist and live data.


🔹 Catalogue

Shows all assets added by the admin.

Each asset is linked to a detailed individual page.


🔹 Individual Asset Page

View historical data and future predictions (1 hour to 1 year).

View data across multiple tabs for different timeframes (1 day, 5 day, 1 month, 1 year)

Predictions stored in DB, not recalculated on every load.


🔹 Watchlist

Logged-in users can add/remove assets to/from their watchlist.

Watchlist items are highlighted on the dashboard.

Feedback messages for already existing or successfully added items.


🔹 Admin Panel

Admin can add new assets (stocks/cryptos) by symbol.

Background job fetches historical data from yfinance api and computes predictions.

Assets automatically show up on dashboard and catalogue.


🔹 Users

Secure Login/Signup system using JWT.

Users can view,edit and delte their profile.

Password reset and recovery functionality via email.


📁 Key Components

marketMinds - Django project root.

dashboard - main app: home,catalogue,admin-asset.

users - users app: login,signup, authentication,admin-user.

templates - frontend html files(Jinja Templating).

static - css, images.


📦 Technologies Used

Django 5.x

Bootstrap 5

PostgreSQL

yfinance API - for data fetching

JWT - for authentication

Docker - for containerization

Render - for Deployment

Git - for version control

Cloudinary - for static and media image handling.

LSTM - for forecasting


📌 Future Improvements

Real-time asset price updates via WebSockets

User-defined prediction parameters

Filtering and searching in the catalogue

Mobile-responsive redesign


👤 Author

Name: Darshan Padia

Project: MarketMinds - Stock/Crypto Prediction App

Location: Mumbai, India