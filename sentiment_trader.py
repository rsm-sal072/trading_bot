import pandas as pd
import alpaca_trade_api as tradeapi

class SentimentTrader:
    def __init__(self, api_key, api_secret, base_url):
        self.api = tradeapi.REST(api_key, 
                                 api_secret, 
                                 base_url, 
                                 api_version='v2')

    def process_sentiment(self, sentiment_data):
        # Assuming sentiment_data is a DataFrame, not a CSV file path
        # Identify negative companies and sell their positions
        self.sell_negative_positions(sentiment_data)

        # Map dollar amounts to time periods, buy for positive sentiments
        self.buy_positive_positions(sentiment_data)

    def sell_negative_positions(self, sentiment_df):
        # Filter for negative sentiment
        negative_companies = sentiment_df[sentiment_df['summary_sentiment'].str.lower() == 'negative']['symbol'].unique()
        
        # Get current positions
        current_positions = self.api.list_positions()

        # Loop through current positions, sell if in the negative companies array
        for position in current_positions:
            symbol = position.symbol
            if symbol in negative_companies:
                print(f"Selling all positions in {symbol}")
                try:
                    self.api.submit_order(
                        symbol=symbol,
                        qty=position.qty,
                        side='sell',
                        type='market',
                        time_in_force='gtc'
                    )
                    print(f"Sold all positions in {symbol}")
                except Exception as e:
                    print(f"An error occurred while selling {symbol}: {e}")

    def buy_positive_positions(self, sentiment_df):
        # Define the dollar amount mapping based on time period
        dollar_amount_time_period_map = {
            'last_hour': 10000,
            'last_eight_hours': 5000,
            'last_sixteen_hours': 2500,
            'last_24_hours': 1000,
            'last_day': 500,
            'last_week': 250
        }

        # Filter for positive sentiment and map the dollar amounts
        sentiment_df_buy = sentiment_df[sentiment_df['summary_sentiment'].str.lower() == 'positive'].copy()
        sentiment_df_buy['notional_to_buy'] = sentiment_df_buy['time_period'].map(dollar_amount_time_period_map)

        # Group by symbol and sum the notional amounts to buy
        sentiment_df_buy = sentiment_df_buy.groupby('symbol', as_index=False)['notional_to_buy'].sum()

        # Loop through the grouped DataFrame and submit buy orders
        for _, row in sentiment_df_buy.iterrows():
            symbol = row['symbol']
            dollar_amount = int(row['notional_to_buy'])
            try:
                order = self.api.submit_order(
                    symbol=symbol,
                    notional=dollar_amount,
                    side='buy',
                    type='market',
                    time_in_force='day'
                )
                print(f"Order submitted successfully for {symbol}: {order}")
            except Exception as e:
                print(f"An error occurred while submitting the order for {symbol}: {e}")

