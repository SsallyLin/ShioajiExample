install: install-poetry
	poetry install

install-poetry:
	pip install poetry

test-cov:
	pytest test --doctest-modules --junitxml=junit/test-results.xml --cov=shioajiexample --cov-report=xml --cov-report=html --cov-report=term