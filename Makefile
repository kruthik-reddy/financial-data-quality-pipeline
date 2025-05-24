install:
	pip install -r requirements.txt

validate:
	python3 scripts/validate_data.py

fetch:
	python3 scripts/fetch_data.py

analyze:
	python3 scripts/analyze_stats.py

test:
	pytest tests/
