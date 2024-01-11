# Binance Trading Automation Script

## Overview
This Python script automates trading on the Binance platform. It uses the Binance API to place market orders, authenticate accounts, and schedule trades. The script is designed to work with a `.env` file for API key management.

## Features
- **Authentication**: Validates Binance API keys.
- **Market Order Placement**: Places market orders with maximum USDT available.
- **Trade Scheduling**: Schedules trades at specified times using APScheduler.
- **Server Time Fetching**: Retrieves the current server time from Binance.
- **Custom Binance Client Class**: A class with methods for various trading actions.

## Requirements
- Python 3
- Binance API Key and Secret
- Required Python libraries: `binance-python`, `apscheduler`, `python-dotenv`

## Installation
1. Clone this repository or download the script.
2. Install required Python libraries:
pip install python-binance apscheduler python-dotenv

javascript
Copy code
3. Create a `.env` file in the same directory as your script with your Binance API key and secret:
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret

python
Copy code

## Usage
1. Ensure the `.env` file with your Binance API credentials is in the same directory as the script.
2. Import the script or use it as a standalone program.
3. Instantiate the `BinanceClient` class with your API key and secret.
4. Use the class methods to perform trading actions.

### Example
```python
from dotenv import load_dotenv
import os
from binance_script import BinanceClient

# Load environment variables
load_dotenv()

# Get API credentials
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

# Check for API credentials
if not api_key or not api_secret:
 raise Exception("API key and secret not set.")

# Create a BinanceClient instance
binance_client = BinanceClient(api_key, api_secret)

# Test authentication
try:
 account_info = binance_client.get_account_info()
 print("Authentication successful. Account information:")
 print(account_info)
except Exception as e:
 print(f"Error: {e}")
Functions and Methods
test_authentication(): Tests Binance API authentication.
place_market_order_with_max_usdt(trading_pair): Places a market order with the maximum available USDT.
schedule_trade_with_apscheduler(function_to_schedule, args, date_string): Schedules a function to run at a specific date and time.
BinanceClient.get_account_info(): Retrieves account information.
BinanceClient.get_server_time(): Fetches the current server time.
BinanceClient.place_market_order(amount, trading_pair, date_string): Places a market order.
BinanceClient.schedule_market_order(amount, trading_pair, date_string): Schedules a market order at a specified time.
Notes
Ensure the script is run in an environment with internet access for API communication.
Handle API rate limits and exceptions appropriately.
Disclaimer
This script is provided as-is, and the use of automated trading scripts carries inherent risks. Users should test thoroughly and understand the implications of automated trading.