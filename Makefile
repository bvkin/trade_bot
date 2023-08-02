.PHONY: test

test:
	python -m unittest discover tests

interactive:
	jupyter notebook trading_interactive.ipynb
