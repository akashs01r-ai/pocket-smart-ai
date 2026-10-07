# PocketSmart AI

PocketSmart AI is a FastAPI budget and recommendation assistant with home,
party, and jewelry planners, account registration and login, saved recommendation
history, and a local recommendation catalog. Gemini is optional; without an API
key, recommendations use the local catalog.

## Run locally on Windows

Open this project folder in VS Code and use a PowerShell terminal from the
project root. Python 3.11 or newer is required.

```powershell
python -m venv .venv
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. The API documentation is at
<http://127.0.0.1:8000/docs>, and the health endpoint is
<http://127.0.0.1:8000/api/health>. Stop the development server with `Ctrl+C`.

The app creates its SQLite database at `data/pocketsmart.db` on first startup.
Gemini is not needed for local use. To enable it, add a Gemini API key to
`.env`; otherwise the built-in local catalog is used.

## Configuration

Copy `.env.example` to `.env` if one does not already exist. `.env` is ignored by
Git. For local development, change `SECRET_KEY` to a private random value. The
database path, allowed local origins, upload size, and optional Gemini settings
can also be configured there.

## Main pages

- `/` — home page
- `/planner/home`, `/planner/party`, `/planner/jewelry` — planners
- `/register` and `/login` — account pages
- `/dashboard` and `/history` — account features
