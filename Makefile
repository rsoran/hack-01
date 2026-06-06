.PHONY: install run clean

install:
	pip install -r requirements.txt

run:
	python backend/app.py

clean:
	rm -rf backend/__pycache__ api/__pycache__
