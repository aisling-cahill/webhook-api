# Telnyx Dynamic Variables Webhook API

A lightweight FastAPI service for handling Telnyx webhooks and querying appointment data.

## Setup

1. **Install dependencies:**
   ```bash
   cd webhook-api
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase connection string
   ```

3. **Run the API:**
   ```bash
   python main.py
   # Or with uvicorn:
   uvicorn main:app --reload --port 8000
   ```

## Usage

The API provides:
- `POST /telnyx-dynamic-vars` - Main webhook endpoint (matches your n8n workflow)
- `GET /health` - Health check endpoint

## Deployment

For production, consider using:
- Docker containerization
- Railway, Heroku, or similar PaaS
- Reverse proxy (nginx) for SSL termination
