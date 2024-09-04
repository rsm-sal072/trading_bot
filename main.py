import os
from dotenv import load_dotenv
from news_advisor_bot import NewsAdvisorBot  # Combined class that handles both news fetching and sentiment analysis
from sentiment_trader import SentimentTrader
from config import SYMBOLS

def main():
    try:
        # Load environment variables from .env file
        load_dotenv()

        # Fetch Alpaca API credentials
        ALPACA_API_KEY = "PKN5131GB4VMX88B1YN7"
        ALPACA_SECRET_KEY = "6fN7wWoehkRV3B4yf1sdkSozQR9NKaRPeUIZVBeS"
        ALPACA_URL = "https://paper-api.alpaca.markets"

        # Debugging: Print the variables to confirm they are loaded
        print(f"ALPACA_API_KEY: {ALPACA_API_KEY}")
        print(f"ALPACA_SECRET_KEY: {ALPACA_SECRET_KEY}")
        print(f"ALPACA_URL: {ALPACA_URL}")

        if not ALPACA_API_KEY or not ALPACA_SECRET_KEY or not ALPACA_URL:
            raise ValueError("API key, secret, or base URL is missing. Please set them in your environment variables.")

        # Run the combined News and Advisor Bot
        print("Running NewsAdvisorBot...")
        bot = NewsAdvisorBot(SYMBOLS)
        sentiment_summary_df = bot.run()  # Get sentiment summary DataFrame directly
        print("NewsAdvisorBot completed.\n")

        # Run the TradeBot
        print("Running TradeBot...")
        trade_bot = SentimentTrader(api_key=ALPACA_API_KEY, api_secret=ALPACA_SECRET_KEY, base_url=ALPACA_URL)
        trade_bot.process_sentiment(sentiment_summary_df)  # Pass DataFrame directly
        print("TradeBot completed.\n")

    except Exception as e:
        print(f"An error occurred in the main sequence: {e}")

if __name__ == "__main__":
    print("Guys... It's worrrkkkiiinnngggg")
    main()
