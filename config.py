from dotenv import load_dotenv, find_dotenv
import os

# Explicitly specify the path to the .env file
load_dotenv(find_dotenv())

ALPACA_API_KEY = os.getenv("APCA_API_KEY_ID")
ALPACA_SECRET_KEY = os.getenv("APCA_API_SECRET_KEY")
ALPACA_URL = os.getenv("APCA_API_BASE_URL")

# Stock symbols to trade
SYMBOLS = ["AAPL", "TSLA", "AMZN", "MSFT", "NVDA", "JPM", "XOM", "CVX", "XAU/USD", "CO1"] 
