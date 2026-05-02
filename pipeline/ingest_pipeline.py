"""
ingest_pipeline.py — fetch → extract → chunk → embed → store

Orchestrates the full ingestion pipeline: downloads papers from arXiv,
extracts text, chunks it, generates embeddings, and stores in ChromaDB.
"""
