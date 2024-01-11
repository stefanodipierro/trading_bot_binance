# Import Required Libraries
from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import time



# Load Environment Variables
load_dotenv()

# Import API Keys
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Ensure that the API key and secret are set
if not api_key or not api_secret:
    raise Exception("API key and secret not set. Please set your Binance API key and secret in the .env file.")

# Create Client Object
client = Client(api_key, api_secret)
print(api_key)

# Scheduler Initialization
scheduler = BackgroundScheduler()


# Test Authentication
def test_authentication():
    try:
        account_info = client.get_account()
        print("Authentication successful. Account information retrieved:")
        print(account_info)
    except Exception as e:
        print("Error in authentication or retrieving account information:")
        print(e)


# Test server time fetching
from binance.client import Client

# Function to test server time
def test_server_time():
    try:
        server_time = client.get_server_time()
        print("Server time retrieved:")
        print(server_time['serverTime'])
    except Exception as e:
        print("Error in retrieving server time:")
        print(e)


# Function to start another function at a given date and time
def schedule_trade_with_apscheduler(function_to_schedule, args, date_string):
    try:
        scheduler.add_job(function_to_schedule, 'date', run_date=date_string, args=args)
        scheduler.start()
        print(f"Function scheduled for {date_string}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Keep the script running indefinitely
    while True:
        time.sleep(1)
        
    







# Function to Place Market Order with Maximum USDT Available

def place_market_order_with_max_usdt(trading_pair):
    order = None  # Assign a default value to order

    try:
        # Fetch account balance for USDT
        usdt_balance = client.get_asset_balance(asset='USDT')
        max_usdt_amount = float(usdt_balance['free'])

        if max_usdt_amount <= 0:
            raise Exception("Insufficient USDT balance to place order.")

        # Place Market Order
        # add retry after 20ms
        counter = 0
        while counter < 10:
            try:
                order = client.order_market_buy(symbol=trading_pair, quoteOrderQty=max_usdt_amount)
                break
            except BinanceAPIException as e:
                counter += 1
                print(f"Binance API Exception: {e.status_code} - {e.message}")
                print(f"Retrying...")
                continue
        
        # If the order is successfully placed wait 500ms
        
        if order is not None:
            # make a sell market order for the maximum amount of the trading pair
            # add retry after 20ms
            counter = 0
            while counter < 5:
                try:
                    order_sell = client.order_market_sell(symbol=trading_pair, quantity=order['executedQty'])
                    break
                except BinanceAPIException as e:
                    counter += 1
                    print(f"Binance API Exception: {e.status_code} - {e.message}")
                    print(f"Retrying in 20ms...")
                    time.sleep(0.02)
                    continue
        

        print(f"Market order placed for max USDT {max_usdt_amount} in {trading_pair} at {order['transactTime']}")
        print(f"Market order sold {trading_pair} for {order_sell['executedQty']} at {order_sell['transactTime']}")
        return order, order_sell
    except BinanceAPIException as e:
        raise Exception(f"Binance API Exception: {e.status_code} - {e.message}")
    



# Note: Ensure the .env file is placed in the same directory as your script.

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_account_info(self):
        try:
            return self.client.get_account()
        except BinanceAPIException as e:
            raise Exception(f"Binance API Exception: {e.status_code} - {e.message}")    
    # Function to Fetch Current Server Time
    
    def get_server_time(self):
        try:
            server_time = self.client.get_server_time()
            return server_time['serverTime']
        except BinanceAPIException as e:
            raise Exception(f"Binance API Exception: {e.status_code} - {e.message}")
    # Method to Convert YYYY-MM-DDTHH:MM:SS to Epoch Milliseconds
    
    def convert_to_milliseconds(self, date_string):
        try:
            return int(datetime.datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").timestamp() * 1000)
        except ValueError as e:
            raise Exception(f"Value Error: {e}")
    
    # Method to that takes an amount as float, a trading pair as string, and a date %Y-%m-%dT%H:%M:%S as string and place a market order for the spot account
    
    def place_market_order(self, amount, trading_pair, date_string):
        try:
            order = self.client.order_market_buy(
                symbol=trading_pair,
                quantity=amount)
            print(f"Market order placed for {amount} {trading_pair} at {date_string}")
            return order
        except BinanceAPIException as e:
            raise Exception(f"Binance API Exception: {e.status_code} - {e.message}")
    
    # Method that schedules a market order to be placed at a given date and time
    # remember to convert the datetime into epoch linux millisecon
    '''Usage Example
    binance_client = BinanceClient(api_key, api_secret)

    datetime_str = "2023-01-01T12:00:00"
    trading_pair = "BTCUSDT"
    amount = 0.01

    binance_client.schedule_trade_with_apscheduler(amount, trading_pair, datetime_str)'''
    
    def schedule_market_order(self, amount, trading_pair, date_string):
        try:
            # Convert datetime string to epoch milliseconds
            trade_epoch_millis = self.convert_to_milliseconds(date_string)
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.place_market_order, 'date', trade_epoch_millis, args=[amount, trading_pair, trade_epoch_millis])
            scheduler.start()
            print(f"Market order scheduled for {amount} {trading_pair} at {date_string}")
        except Exception as e:
            raise Exception(f"Error: {e}")

'''
# Usage Example for BinanceClient Class
# Ensure the .env file is placed in the same directory as your script.
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

if not api_key or not api_secret:
    raise Exception("API key and secret not set.")

binance_client = BinanceClient(api_key, api_secret)

# Test Authentication
try:
    account_info = binance_client.get_account_info()
    print("Authentication successful. Account information:")
    print(account_info)
except Exception as e:
    print(f"Error: {e}")
'''

if __name__ == '__main__':
    schedule_trade_with_apscheduler(place_market_order_with_max_usdt, ['BTCUSDT'], '2024-01-09T19:50:59')





