.PHONY: all clean lint type test test-cov pretty poetry-download

CMD:=poetry run
PYMODULE:=j5
TESTS:=tests

poetry-download:
	curl -sSL https://install.python-poetry.org | python -

all: type test lint

lint:
	$(CMD) mypy --install-types --non-interactive ./semantic_shifts

pretty:
	$(CMD) pyupgrade --exit-zero-even-if-changed --py310-plus **/*.py
	$(CMD) isort --settings-path pyproject.toml ./
	$(CMD) black --config pyproject.toml ./
	$(CMD) autoflake --in-place --remove-unused-variables --remove-all-unused-imports --expand-star-imports --ignore-init-module-imports --remove-duplicate-keys -r ./semantic_shifts ./tests

run:
	$(CMD) python -m semantic_shifts

type:
	$(CMD) mypy $(PYMODULE) $(TESTS)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

test-cov:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report html

clean:
	git clean -Xdf # Delete all files in .gitignore