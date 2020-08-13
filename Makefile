bootstrap:
	rm -rf ./env
	virtualenv -p python3 env
	source env/bin/activate && poetry install --extras all

test:
	pytest -s --ff tests
	pytest src
