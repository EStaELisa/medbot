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

download-data: # Download data from the internet, NEEDS TO BE IMPLEMENTED
	@wget https://github.com/MIT-LCP/mimic-code/archive/refs/heads/main.zip -O mimic-code.zip # repo for MIMIC-IV for migrating to PostgreSQL (mimic iv missing?)
	@unzip mimic-code.zip && rm mimic-code.zip

	@wget -r -N -c -np https://physionet.org/files/mimic-iv-demo/2.2/
