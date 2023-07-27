# trade_bot
Bot to automatically manage a stock portfolio

## Installation
### Install required packages
pip install -r requirements.txt

## Usage
### Local
This project uses the Alpaca Api to manage trades in the [Alpaca](https://alpaca.markets/) brokerage. 
1. Create a `.env` file and for api keys. Directoions in [docs](https://alpaca.markets/learn/connect-to-alpaca-api/). Populate like the following:
```
ALPACA_API_KEY="your_alpaca_api_key"
ALPACA_SECRET_KEY="your_alpaca_secret_key"
```
2. Run the bot
```
python trade_bot/main.py
```

## Tests
You can run test cases using make
```
make test
```
