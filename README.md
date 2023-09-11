# trade_bot

Bot to automatically manage a stock portfolio
Installation
Install required packages

pip install -r requirements.txt
Usage
Local

This project uses the Alpaca Api to manage trades in the Alpaca brokerage.

    Create a .env file and for api keys. Directions in docs. Populate like the following:

ALPACA_API_KEY="your_alpaca_api_key"
ALPACA_SECRET_KEY="your_alpaca_secret_key"

<<<<<<< HEAD
    Run the bot

python trade_bot/main.py

## Documentation (Written by Bard).
### Trading Strategy & Insights (From the code).

The trading strategy is specified in the make_orders() function. This function takes three arguments:

A TradeManager instance, which is used to make orders. An SNSClient instance, which is used to publish messages to an SNS topic. The ARN of the SNS topic. The make_orders() function first gets the list of all the stocks in the S&P 500. Then, it iterates over the list of stocks and generates a buy or sell signal for each stock based on the moving average crossover strategy or the engulfing candlestick pattern strategy. If the signal is a buy signal, the function places a buy order for the stock. If the signal is a sell signal, the function places a sell order for the stock.

The AlpacaTradeManager class is used to make orders. This class abstracts away the details of interacting with the Alpaca API. The SNSClient class is used to publish messages to an SNS topic. An SNS topic is a way to decouple senders and receivers of messages.

The make_orders() function is scheduled to run every day at 9am EST using the apscheduler library. The apscheduler library is a Python library that is used to schedule recurring tasks.

The Alpaca API interprets the trading strategy by placing orders on the user's behalf. The Alpaca API is a RESTful API that allows users to trade stocks, options, and futures.

Here is an example of how the trading strategy would be interpreted by the Alpaca API for a stock called AAPL:

If the moving average crossover strategy is used and the 5-day moving average crosses above the 20-day moving average, the Alpaca API would place a buy order for AAPL. If the engulfing candlestick pattern strategy is used and the open price of a day is lower than the previous day's close price and the close price of the day is higher than the previous day's open price, the Alpaca API would place a buy order for AAPL. If the moving average crossover strategy is used and the 5-day moving average crosses below the 20-day moving average, the Alpaca API would place a sell order for AAPL. If the engulfing candlestick pattern strategy is used and the open price of a day is higher than the previous day's close price and the close price of the day is lower than the previous day's open price, the Alpaca API would place a sell order for AAPL.

### Trading Strategies...
### Trading Strategy 1 (Moving Average Crossover)

The moving average crossover strategy is a technical analysis trading strategy that uses moving averages to identify buy and sell signals. A moving average is a line that smooths out the price data by taking the average price over a specified period of time.

The moving average crossover strategy works by looking for when the short-term moving average crosses above the long-term moving average. This is interpreted as a signal that the trend is changing from down to up, and a buy signal is generated.

The opposite is true when the short-term moving average crosses below the long-term moving average. This is interpreted as a signal that the trend is changing from up to down, and a sell signal is generated.

The moving average crossover strategy is a simple and easy-to-use trading strategy, but it is not without its risks. The strategy can generate false signals, and it is important to use other technical analysis tools to confirm the signals.

Here are some of the advantages of the moving average crossover strategy:

It is a simple and easy-to-use strategy. It is a trend-following strategy, which means that it can help you to identify trends early. It is a relatively low-risk strategy. Here are some of the disadvantages of the moving average crossover strategy:

It can generate false signals. It is not as effective in volatile markets. It is not a good strategy for short-term trading. Overall, the moving average crossover strategy is a good starting point for traders who are new to technical analysis. It is a simple and easy-to-use strategy that can help you to identify trends early. However, it is important to use other technical analysis tools to confirm the signals and to manage your risk.

### Trading Strategy 2 (Engulfing Candlestick Pattern)

The engulfing candlestick pattern is a reversal pattern that can be used to identify buy and sell signals.

An engulfing candlestick pattern is formed when a candle completely engulfs the previous candle. The engulfing candle can be either bullish or bearish.

A bullish engulfing candlestick pattern is formed when a white candle completely engulfs a black candle. This is interpreted as a signal that the trend is changing from down to up, and a buy signal is generated.

A bearish engulfing candlestick pattern is formed when a black candle completely engulfs a white candle. This is interpreted as a signal that the trend is changing from up to down, and a sell signal is generated.

The engulfing candlestick pattern is a relatively simple and easy-to-use trading strategy, but it is not without its risks. The strategy can generate false signals, and it is important to use other technical analysis tools to confirm the signals.

Here are some of the advantages of the engulfing candlestick pattern trading strategy:

It is a simple and easy-to-use strategy. It is a reversal pattern, which means that it can help you to identify trend reversals early. It is a relatively low-risk strategy. Here are some of the disadvantages of the engulfing candlestick pattern trading strategy:

It can generate false signals. It is not as effective in volatile markets. It is not a good strategy for short-term trading. Overall, the engulfing candlestick pattern trading strategy is a good starting point for traders who are new to technical analysis. It is a simple and easy-to-use strategy that can help you to identify trend reversals early. However, it is important to use other technical analysis tools to confirm the signals and to manage your risk.

Here are some additional things to keep in mind when using the engulfing candlestick pattern trading strategy:

The engulfing candle should be large in size. The engulfing candle should have a strong close. The engulfing candle should be confirmed by other technical analysis tools. By following these tips, you can increase the chances of success when using the engulfing candlestick pattern trading strategy.

### File Specification
#### main.py

=======
### Docs

#### main.py
>>>>>>> a5ed8e9 (readme first draft)
This file is a Python script that uses the Alpaca Trade Manager and APScheduler libraries to place orders on the stock market.

The first few lines of the script set up the logging configuration. The logging.basicConfig() function sets the global logging level to INFO, and the apscheduler_logger.setLevel(logging.WARNING) function sets the logging level for the apscheduler.scheduler logger to WARNING.

The next few lines of code load the environment variables for the ALPACA_API_KEY, ALPACA_SECRET_KEY, AWS_DEFAULT_REGION, and AWS_SNS_TOPIC_ARN environment variables. These environment variables are used to connect to the Alpaca API, the AWS SNS service, and the AWS SNS topic.

The make_orders() function is used to place orders on the stock market. This function takes three arguments: the AlpacaTradeManager object, the SNS client object, and the SNS topic ARN. The make_orders() function uses the AlpacaTradeManager object to get the current market data and then places orders based on the trading strategy.

The get_first_last_market_days() function is used to get the first and last market days of the current week. This function is used by the scheduler.add_job() function to schedule the make_orders() function to run every Monday morning at 9:00 AM Eastern Time.

The scheduler.add_job() function schedules the make_orders() function to run every Monday morning at 9:00 AM Eastern Time. The scheduler.add_job() function takes four arguments: the function to run, the schedule, the arguments to pass to the function, and the start date.

The scheduler.start() function starts the scheduler.

<<<<<<< HEAD
The name == 'main' statement ensures that the script only runs when it is executed as a script, not when it is imported as a module.

#### trading.py

=======
The __name__ == '__main__' statement ensures that the script only runs when it is executed as a script, not when it is imported as a module.

#### trading.py
>>>>>>> a5ed8e9 (readme first draft)
This file contains a simple trading bot that generates buy and sell signals for the S&P 500 stocks.

The bot uses two trading strategies:

<<<<<<< HEAD
    Moving average crossover strategy: This strategy buys a stock when the 5-day moving average crosses above the 20-day moving average and sells the stock when the 5-day moving average crosses below the 20-day moving average.
    Engulfing candlestick pattern strategy: This strategy buys a stock when the open price of a day is lower than the previous day's close price and the close price of the day is higher than the previous day's open price.

The bot makes orders through the TradeManager class, which abstracts away the details of interacting with a brokerage account.

To use the bot, you will need to create a TradeManager instance and pass it to the make_orders() function. The make_orders() function will generate buy and sell signals for all the stocks in the S&P 500 and place the appropriate orders.

Here is an example of how to use the bot:

import trade_bot

#### Create a TradeManager instance
trade_manager = trade_bot.TradeManager()

#### Generate buy and sell signals
=======
* **Moving average crossover strategy:** This strategy buys a stock when the 5-day moving average crosses above the 20-day moving average and sells the stock when the 5-day moving average crosses below the 20-day moving average.
* **Engulfing candlestick pattern strategy:** This strategy buys a stock when the open price of a day is lower than the previous day's close price and the close price of the day is higher than the previous day's open price.

The bot makes orders through the `TradeManager` class, which abstracts away the details of interacting with a brokerage account.

To use the bot, you will need to create a `TradeManager` instance and pass it to the `make_orders()` function. The `make_orders()` function will generate buy and sell signals for all the stocks in the S&P 500 and place the appropriate orders.

Here is an example of how to use the bot:

```python
import trade_bot

# Create a TradeManager instance
trade_manager = trade_bot.TradeManager()

# Generate buy and sell signals
>>>>>>> a5ed8e9 (readme first draft)
trade_bot.make_orders(trade_manager)


The `make_orders()` function will print out the tickers of the stocks that were bought and sold. It will also publish a message to an SNS topic with the list of stocks that were traded.
<<<<<<< HEAD

#### alpaca_trade_manager.py

This file defines a class called AlpacaTradeManager. This class provides methods to interact with the Alpaca API, such as getting price data, buying stocks, and selling stocks.

The init() method initializes the AlpacaTradeManager object. The api attribute is a REST object that is used to interact with the Alpaca API.
=======
```

<<<<<<< HEAD
=======
### Docs

#### main.py
This file is a Python script that uses the Alpaca Trade Manager and APScheduler libraries to place orders on the stock market.

The first few lines of the script set up the logging configuration. The logging.basicConfig() function sets the global logging level to INFO, and the apscheduler_logger.setLevel(logging.WARNING) function sets the logging level for the apscheduler.scheduler logger to WARNING.

The next few lines of code load the environment variables for the ALPACA_API_KEY, ALPACA_SECRET_KEY, AWS_DEFAULT_REGION, and AWS_SNS_TOPIC_ARN environment variables. These environment variables are used to connect to the Alpaca API, the AWS SNS service, and the AWS SNS topic.

The make_orders() function is used to place orders on the stock market. This function takes three arguments: the AlpacaTradeManager object, the SNS client object, and the SNS topic ARN. The make_orders() function uses the AlpacaTradeManager object to get the current market data and then places orders based on the trading strategy.

The get_first_last_market_days() function is used to get the first and last market days of the current week. This function is used by the scheduler.add_job() function to schedule the make_orders() function to run every Monday morning at 9:00 AM Eastern Time.

The scheduler.add_job() function schedules the make_orders() function to run every Monday morning at 9:00 AM Eastern Time. The scheduler.add_job() function takes four arguments: the function to run, the schedule, the arguments to pass to the function, and the start date.

The scheduler.start() function starts the scheduler.

The __name__ == '__main__' statement ensures that the script only runs when it is executed as a script, not when it is imported as a module.

#### trading.py
This file contains a simple trading bot that generates buy and sell signals for the S&P 500 stocks.

The bot uses two trading strategies:

* **Moving average crossover strategy:** This strategy buys a stock when the 5-day moving average crosses above the 20-day moving average and sells the stock when the 5-day moving average crosses below the 20-day moving average.
* **Engulfing candlestick pattern strategy:** This strategy buys a stock when the open price of a day is lower than the previous day's close price and the close price of the day is higher than the previous day's open price.

The bot makes orders through the `TradeManager` class, which abstracts away the details of interacting with a brokerage account.

To use the bot, you will need to create a `TradeManager` instance and pass it to the `make_orders()` function. The `make_orders()` function will generate buy and sell signals for all the stocks in the S&P 500 and place the appropriate orders.

Here is an example of how to use the bot:

```python
import trade_bot

# Create a TradeManager instance
trade_manager = trade_bot.TradeManager()

# Generate buy and sell signals
trade_bot.make_orders(trade_manager)


The `make_orders()` function will print out the tickers of the stocks that were bought and sold. It will also publish a message to an SNS topic with the list of stocks that were traded.
```

>>>>>>> bab243f (readme first draft)
#### alpaca_trade_manager.py
This file defines a class called AlpacaTradeManager. This class provides methods to interact with the Alpaca API, such as getting price data, buying stocks, and selling stocks.

The __init__() method initializes the AlpacaTradeManager object. The api attribute is a REST object that is used to interact with the Alpaca API.
<<<<<<< HEAD
>>>>>>> a5ed8e9 (readme first draft)
=======
>>>>>>> bab243f (readme first draft)

The get_price_data() method returns a pandas dataframe of the price data for the last two days of a given ticker.

The buy_stock() method buys 5% of the buying power of the account for a given ticker. The stop_loss parameter specifies the price at which the order should be sold if the price of the stock falls below that level.

The sell_stock() method sells all shares of a given stock.

The get_stock_qty() method returns the quantity of a stock owned.

The get_owned_tickers() method returns a list of tickers currently held in account.
<<<<<<< HEAD
<<<<<<< HEAD
Tests

=======
=======
>>>>>>> bab243f (readme first draft)

### 

## Tests
>>>>>>> a5ed8e9 (readme first draft)
You can run test cases using make

make tests

