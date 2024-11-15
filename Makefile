SHELL=/bin/bash -e -o pipefail

.PHONY: test
test: # Runs all unit tests in the folder test
	@pytest -v tests/

lint: # Lint code, checks python conventions
	@flake8 .

check-format: # Check code format
	@black --check .

format: # Format code, formats code automatically, needs to be called if wanted
	@black .

ci: test lint check-format