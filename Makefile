brunette:
	brunette pamatnikpandemie tests config.py setup.py

flake:
	flake8 pamatnikpandemie tests config.py setup.py

test:
	pytest

check: brunette flake #test

install-dev:
	python -m pip install virtualenv
	python -m virtualenv venv
	source venv/bin/activate && python -m pip install -e ".[dev]"
	source venv/bin/activate && pre-commit install
	source venv/bin/activate && python -m pip install ipykernel
	source venv/bin/activate && ipython kernel install --user --name=pamatnikpandemie

install-test:
	python -m pip install -e ".[test]"

clean:
	rm -rf build __pycache__ pamatnikpandemie/__pycache__ __pycache__ instance \
	tests/__pycache__ tests/pamatnikpandemie/__pycache__ .pytest_cache *.egg-info .eggs tests/pamatnikpandemie/__pycache__\
	tests/pamatnikpandemie/toolkit/__pycache__ tests/pamatnikpandemie/toolkit/testing/__pycache__ \
	pamatnikpandemie/toolkit/__pycache__ pamatnikpandemie/toolkit/testing/__pycache__ \
	pamatnikpandemie/toolkit/testing/resources/__pycache__ pamatnikpandemie/toolkit/testing/avast/__pycache__ \
	tests/pamatnikpandemie/server/__pycache__ tests/pamatnikpandemie/toolkit/__pycache__  tests/pamatnikpandemie/toolkit/avast/__pycache__ \
	pamatnikpandemie/toolkit/testing/avast/resources/__pycache__

locust:
	locust -f tests/locust.py --headless --host https://admin.pamatnikpandemie.cz -u 50 -r 5

locust-web:
	locust -f tests/locust_web.py --headless --host https://www.pamatnikpandemie.cz -u 50 -r 5
