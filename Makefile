setup:
	pip install -r requirements.txt

ingest:
	python -m pipeline.ingest_pipeline

run:
	streamlit run app/main.py

test:
	pytest tests/ -v

clean:
	rm -rf chroma_db/ papers/