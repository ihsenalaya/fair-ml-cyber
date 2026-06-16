.PHONY: setup test lint audit smoke clean

PYTHON ?= python3
CSV_DIR ?= /mnt/c/Users/IhsenAlaya/Documents/ihsen/fhir/CSVs/CSVs
WORK_DIR ?= data

setup:
	$(PYTHON) -m pip install -e ".[dev]"

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m ruff check src tests

audit:
	$(PYTHON) -m fair_ml_cyber.cli audit --csv-dir "$(CSV_DIR)" --output-dir "$(WORK_DIR)/audit"

smoke:
	$(PYTHON) -m fair_ml_cyber.cli run-smoke --csv-dir "$(CSV_DIR)" --work-dir "$(WORK_DIR)/smoke" --sample-per-file 2000

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info
	find . -type d -name __pycache__ -prune -exec rm -rf {} +

