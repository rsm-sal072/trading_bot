from dotenv import load_dotenv, find_dotenv
import os

# Explicitly specify the path to the .env file
load_dotenv(find_dotenv())

ALPACA_API_KEY = PK9O1OCIJFWP1Y10UCZH
ALPACA_SECRET_KEY = AfyweADMdPUIWcodotseAwxJbdbhlJpn4xkT7wP6
ALPACA_URL = https://paper-api.alpaca.markets

# Stock symbols to trade
SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META", "LLY", "AVGO", "TSLA", "LMT", "EA", "CRM", "OXY"]  
