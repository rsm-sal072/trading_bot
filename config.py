from dotenv import load_dotenv, find_dotenv
import os

# Explicitly specify the path to the .env file
load_dotenv(find_dotenv())

ALPACA_API_KEY = PKSMGL3DXLBX2ROOJ3YF
ALPACA_SECRET_KEY = mL7hpYPj2Bdb7rMPrOwcbYYSuiWIxcKZa9RIMJay
ALPACA_URL = https://paper-api.alpaca.markets

# Stock symbols to trade
SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "LLY", "AVGO", "TSLA", "LMT", "EA", "CRM", "OXY"]  
