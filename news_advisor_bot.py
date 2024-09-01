def place_order(self, symbol, amount):
    try:
        # Ensure the amount is exactly $1 or -$1 before placing an order
        if abs(amount) != 1:
            print(f"Warning: Invalid order amount: {amount}. It should be exactly $1 or -$1.")
            return

        print(f"Placing an order for {symbol}: ${amount}")
        
        # Check for buy or sell and ensure it's a notional trade of $1
        if amount > 0:
            self.alpaca.submit_order(
                symbol=symbol,
                notional=1,  # Buy exactly $1 worth of stock
                side='buy',
                type='market',
                time_in_force='gtc'
            )
        elif amount < 0:
            self.alpaca.submit_order(
                symbol=symbol,
                notional=1,  # Sell exactly $1 worth of stock
                side='sell',
                type='market',
                time_in_force='gtc'
            )
    except Exception as e:
        print(f"Error placing order for {symbol}: {e}")
