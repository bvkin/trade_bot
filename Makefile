.PHONY: test

test:
	coverage run -m unittest discover tests
	coverage report -m --fail-under=70

build:
	docker build -f docker/Dockerfile . -t trade_bot
