brunette:
	brunette pomnicek tests config.py setup.py

flake:
	flake8 pomnicek tests config.py setup.py

test:
	pytest

check: brunette flake #test

install-dev:
	python -m pip install virtualenv
	python -m virtualenv venv
	source venv/bin/activate && python -m pip install -e ".[dev]"
	source venv/bin/activate && pre-commit install
	source venv/bin/activate && python -m pip install ipykernel
	source venv/bin/activate && ipython kernel install --user --name=pomnicek

install-test:
	python -m pip install -e ".[test]"

clean:
	rm -rf build __pycache__ pomnicek/__pycache__ __pycache__ instance \
	tests/__pycache__ tests/pomnicek/__pycache__ .pytest_cache *.egg-info .eggs tests/pomnicek/__pycache__\
	tests/pomnicek/toolkit/__pycache__ tests/pomnicek/toolkit/testing/__pycache__ \
	pomnicek/toolkit/__pycache__ pomnicek/toolkit/testing/__pycache__ \
	pomnicek/toolkit/testing/resources/__pycache__ pomnicek/toolkit/testing/avast/__pycache__ \
	tests/pomnicek/server/__pycache__ tests/pomnicek/toolkit/__pycache__  tests/pomnicek/toolkit/avast/__pycache__ \
	pomnicek/toolkit/testing/avast/resources/__pycache__

locust:
	locust -f tests/locust.py --headless --host https://pomnicek.herokuapp.com -u 100 -r 5
