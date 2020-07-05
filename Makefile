test:
	pytest tests/

clean:
	find . -name '*.pyc' -execdir rm -f {} +
	find . -type d -name '__pycache__' -execdir rm -rf {} +
	find . -name '*.log' -execdir rm -f {} +
	python setup clean --all

black:
	black p66/
	black tests/unit/

build:
	python setup.py sdist bdist_wheel

.PHONY: test clean black build
