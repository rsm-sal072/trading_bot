import os
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import requests
import re
import pandas as pd
import warnings
import random
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from collections import Counter
from pytz import UTC
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_URL, SYMBOLS

warnings.filterwarnings("ignore")

ALPACA_API_KEY = "PK9O1OCIJFWP1Y10UCZH"
ALPACA_SECRET_KEY = "AfyweADMdPUIWcodotseAwxJbdbhlJpn4xkT7wP6"
ALPACA_URL = "https://paper-api.alpaca.markets"

class NewsAdvisorBot:
    def __init__(self, symbols):
        self.symbols = symbols
        self.columns = ["created_at", "headline", "id", "summary", "symbols"]
        self.alpaca = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, base_url=ALPACA_URL)
        print(f"NewsAdvisorBot initialized.")

        # Load FinBERT model and tokenizer
        print("Loading FinBERT model and tokenizer...")
        self.tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        self.model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
        self.finbert = pipeline('sentiment-analysis', model=self.model, tokenizer=self.tokenizer)
        print("FinBERT model and tokenizer loaded successfully.")

        # List of time periods for aggregation
        self.time_periods = {
            'last_hour': timedelta(hours=1),
            'last_eight_hours': timedelta(hours=8),
            'last_sixteen_hours': timedelta(hours=16),
            'last_24_hours': timedelta(hours=24),
            'last_day': timedelta(days=1),
            'last_week': timedelta(weeks=1)
        }

    def get_news(self, symbol, total_limit=1000):
        print(f"Fetching news for symbol: {symbol}")
        today = datetime.utcnow()
        last_week = today - timedelta(days=7)
        url = "https://data.alpaca.markets/v1beta1/news?include_content=true"
        headers = {
            "APCA-API-KEY-ID": ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
        }
        all_articles = []

        while len(all_articles) < total_limit:
            params = {
                "symbols": symbol,
                "start": last_week.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "end": today.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "limit": 50,  # Maximum allowed per request
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f"Error fetching news for {symbol}: {response.status_code} - {response.text}")
                break

            articles_json = response.json()
            articles = articles_json.get('news', [])
            all_articles.extend(articles)

            if len(articles) < 50:
                # No more pages of articles left
                break

        # If more articles were fetched than the total_limit, randomly sample
        if len(all_articles) > total_limit:
            all_articles = random.sample(all_articles, total_limit)

        print(f"Fetched {len(all_articles)} articles for {symbol}.")
        return {"news": all_articles}

    @staticmethod
    def clean_text(text):
        if not text:
            return text
        text = re.sub(r'&[^;\s]+;', '', text)
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def process_news(self, symbol):
        print(f"Processing news for {symbol}...")
        articles_json = self.get_news(symbol)
        if articles_json:
            articles = articles_json.get('news', [])
            df = pd.DataFrame(articles)
            if df.empty:
                print(f"No articles found for {symbol}.")
                return df

            columns_to_keep = ["created_at", "headline", "id", "summary", "symbols"]
            columns_present = [col for col in columns_to_keep if col in df.columns]
            df = df[columns_present]

            # Convert 'created_at' to datetime with UTC timezone
            df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(UTC)

            df['summary'] = df['summary'].apply(self.clean_text)

            # Ensure 'symbols' is always a list
            df['symbols'] = df['symbols'].apply(lambda x: eval(x) if isinstance(x, str) else x)

            print(f"Processed {len(df)} articles for {symbol}.")
            return df
        return pd.DataFrame(columns=self.columns)

    def apply_sentiment_analysis(self, df):
        print("Applying sentiment analysis to headlines and summaries...")

        # Apply FinBERT sentiment analysis to 'headline' column
        df['headline_sentiment'] = df['headline'].apply(self.get_sentiment_label)

        # Apply FinBERT sentiment analysis to 'summary' column only if it's not null or empty
        df['summary_sentiment'] = df['summary'].apply(lambda x: self.get_sentiment_label(x) if pd.notnull(x) and x != '' else None)

        print("Sentiment analysis completed.")
        return df

    def get_sentiment_label(self, text):
        if pd.isnull(text) or text == '':
            return None
        result = self.finbert(text)
        if result:
            return result[0]['label']
        return None

    def aggregate_sentiment_labels(self, df, symbol, time_delta):
        end_time = datetime.utcnow().replace(tzinfo=UTC)  # Make timezone-aware
        start_time = end_time - time_delta
        print(f"Aggregating sentiment for {symbol} from {start_time} to {end_time}...")

        filtered_df = df[(df['created_at'] >= start_time) & (df['created_at'] <= end_time) & (df['symbols'].apply(lambda x: symbol in x))]

        headline_labels = filtered_df['headline_sentiment'].dropna().tolist()
        summary_labels = filtered_df['summary_sentiment'].dropna().tolist()

        most_common_headline_label = Counter(headline_labels).most_common(1)[0][0] if headline_labels else "No Data"
        most_common_summary_label = Counter(summary_labels).most_common(1)[0][0] if summary_labels else "No Data"

        print(f"Most common headline sentiment: {most_common_headline_label}, Most common summary sentiment: {most_common_summary_label}")
        return most_common_headline_label, most_common_summary_label

    def generate_sentiment_summary(self, df):
        print("Generating sentiment summary...")
        summary_rows = []

        for symbol in self.symbols:
            print(f"Processing symbol: {symbol}")
            for period_name, time_delta in self.time_periods.items():
                most_common_headline_label, most_common_summary_label = self.aggregate_sentiment_labels(df, symbol, time_delta)
                summary_rows.append({
                    'symbol': symbol,
                    'time_period': period_name,
                    'headline_sentiment': most_common_headline_label,
                    'summary_sentiment': most_common_summary_label
                })

        # Convert sentiment summary to a DataFrame
        summary_df = pd.DataFrame(summary_rows)
        print("Sentiment summary generated successfully.")
        return summary_df

    def run(self):
        all_news_data = []
        for symbol in self.symbols:
            df = self.process_news(symbol)
            if not df.empty:
                all_news_data.append(df)
        
        # Combine all data into one DataFrame
        if all_news_data:
            combined_df = pd.concat(all_news_data, ignore_index=True)
            combined_df = self.apply_sentiment_analysis(combined_df)
            sentiment_summary_df = self.generate_sentiment_summary(combined_df)
            return sentiment_summary_df
        else:
            print("No news data available.")
            return pd.DataFrame()

if __name__ == "__main__":
    try:
        bot = NewsAdvisorBot(SYMBOLS)
        sentiment_summary_df = bot.run()
        print(sentiment_summary_df)
    except Exception as e:
        print(f"Error in main: {e}")
