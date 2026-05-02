setup:
	pip install -r requirements.txt
	ollama pull nomic-embed-text

ingest:
	python -m pipeline.ingest_pipeline

run:
	streamlit run app/main.py

test:
	pytest tests/ -v

clean:
	rm -rf chroma_db/ papers/