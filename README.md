# DocuMind: RAG System with Endee Vector DB

DocuMind is a production-grade Semantic Search application built to demonstrate the capabilities of **[Endee](https://github.com/EndeeLabs/endee)**. It features a full-stack architecture with a Streamlit UI, Dockerized infrastructure, and a robust Python client.

## 🚀 Features
* **Vector Engine:** Uses Endee (C++ backend) for millisecond-latency retrieval.
* **Ingestion Pipeline:** Automatic PDF parsing, chunking, and embedding (using `all-MiniLM-L6-v2`).
* **Interactive UI:** Streamlit frontend for file uploads and live querying.
* **Production Ready:** Includes Docker Compose, environment configuration, and modular code.

## 🛠️ System Architecture

1.  **Frontend:** Streamlit (`src/app.py`)
2.  **ETL Layer:** Python (`src/ingest.py`)
3.  **Database:** Endee Server (Running via Docker)

## ⚡ Quick Start

### 1. Start the Endee Database
```bash
docker-compose up -d