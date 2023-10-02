.PHONY: test

test:
	pytest --cov=./trade_bot --cov-fail-under=70 tests

build:
	docker build -f docker/Dockerfile . -t trade_bot
