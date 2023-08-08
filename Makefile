.PHONY: test

test:
	coverage run -m unittest discover tests
	coverage report -m --fail-under=70
