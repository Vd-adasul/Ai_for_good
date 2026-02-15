# AI for Good - Farmer Advisory Bot

This is the backend for the Farmer Advisory Bot, built with FastAPI, LangChain, and Firebase.

## Prerequisites

1.  **Python 3.10+**
2.  **Virtual Environment** (Recommended)
3.  **Firebase Service Account Key**: Place `serviceAccountKey.json` in this directory.
4.  **Environment Variables**: data in `.env` file.

## Installation

```bash
pip install -r requirements.txt
pip install langchain-groq jinja2 python-multipart faster-whisper
```

## Data Processing (RAG)

Before running the app, ensure you have processed the PDFs to create the Knowledge Base:

```bash
# From the 'final project' directory:
python scripts/process_pdfs.py
```
This creates/updates the `faiss_index` folder.

## Running the Server

Run the FastAPI server using Uvicorn:

```bash
# Make sure you are in the 'final project' directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## accessing the App

- **Admin Dashboard**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **WhatsApp Webhook**: [http://localhost:8000/whatsapp/bot](http://localhost:8000/whatsapp/bot) (Needs ngrok for public access)
- **IVR Webhook**: [http://localhost:8000/ivr/welcome](http://localhost:8000/ivr/welcome) (Needs ngrok for public access)

## Exposing to Internet (ngrok)

To test with actual WhatsApp/Twilio:

```bash
ngrok http 8000
```
Then update your Twilio Sandbox URL to the ngrok URL (e.g., `https://<id>.ngrok.io/whatsapp/bot`).
