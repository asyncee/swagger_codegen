bootstrap:
	rm -rf .venv
	poetry install --extras all

test:
	pytest -s --ff tests
	pytest src

style:
	isort src example tests
	black src example tests

lint:
	poetry run flake8 src
