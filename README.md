# trade_bot
Bot to automatically manage a stock portfolio

## Requrements
This project is compatible with python 3.11.4. If you are managing multiple python projects/versions locally, pairing [pyenv](https://github.com/pyenv/pyenv) with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) is one approach that works well for this

## Installation
### Installing required packages
```
 pip install --no-cache-dir . --upgrade pip
 ```

## Usage
### Alpaca
This project uses the Alpaca Api to manage trades in the [Alpaca](https://alpaca.markets/) brokerage. You will need to generate a set of keys to use with the alpaca api. Directoions in their [docs](https://alpaca.markets/learn/connect-to-alpaca-api/). Your keys should be set as the following environment variables:
```
ALPACA_API_KEY="your_alpaca_api_key"
ALPACA_SECRET_KEY="your_alpaca_secret_key"
```
Alternatively, you can create a `.env` and set the values in there.

### AWS
The trade bot is capable of sending email push notifications about stocks it trades. This is handled via [AWS SNS](https://docs.aws.amazon.com/sns/latest/dg/welcome.html). You can create an SNS topic in the AWS Console, or via the automation provided in terraform. For the bot to access your SNS topic, you must provide a means of authentication in the [credentials provider chain](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html#configuring-credentials). The SNS topic arn should be set in the following environment variable:
```
AWS_SNS_TOPIC_ARN
```

### Starting the trade bot
The entrypoint for the trade bot is the `main.py` file located in the `trade_bot` module inside this repo. Visit the module [README.md](./trade_bot/README.md) for startup instructions.

## Tests
Tests can be run locally using `make`:
```
make test
```
Additionally these tests will be run on pull requests and merges to main via github actions.