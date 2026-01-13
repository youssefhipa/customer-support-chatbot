# Customer Support Chatbot Demo

A clean, production-style demo showing a customer support chatbot that calls an LLM through an OpenAI-compatible proxy.

## Setup

1) Create and activate a virtual environment.
2) Create `.env` from the example and set your API key:

```bash
cp .env.example .env
```

3) Install dependencies:

```bash
pip install -r requirements.txt
```

## Start the app

1) Start the backend:

```bash
uvicorn backend.app.main:app --reload --port 8000
```

2) Start the frontend (in a new terminal):

```bash
streamlit run frontend/app.py
```

## Open from another device on the same network

1) Run the backend and frontend on all interfaces:

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
streamlit run frontend/app.py --server.address 0.0.0.0 --server.port 8501
```

2) Find your laptop's local IP address (for example, `192.168.1.25`).

3) Open the frontend on the other device:

```
http://YOUR_LAN_IP:8501
```

4) Ensure your firewall allows ports `8000` and `8501`.

## Run the backend

```bash
uvicorn backend.app.main:app --reload --port 8000
```

## Run the frontend

```bash
streamlit run frontend/app.py
```

## Configuration

The backend calls an OpenAI-compatible chat completion endpoint via a proxy URL built from `PROXY_BASE_URL` and `PROXY_CHAT_PATH` in `.env`.
