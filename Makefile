bootstrap:
	rm -rf .venv
	poetry install --extras all

test:
	poetry run pytest -s --ff tests
	poetry run pytest src

style:
	poetry run isort src example tests
	poetry run black src example tests

lint:
	poetry run flake8 src
