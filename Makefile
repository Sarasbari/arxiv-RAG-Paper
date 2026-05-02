ingest:
	python -m pipeline.ingest_pipeline

run:
	streamlit run app/main.py

test:
	pytest tests/ -v

setup:
	pip install -r requirements.txt && ollama pull nomic-embed-text