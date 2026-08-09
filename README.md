# Drama Companion

A terminal-based drama companion. There is **no Streamlit UI or web server**
in the current version.

## What it does

- Classifies messages as chat, question, review, or recommendation.
- Keeps a small amount of recent conversation context.
- Stores drama data and user reactions in SQLite.
- Uses Gemini for conversation and review/preference extraction.
- Uses stored preferences when generating future responses.

## Setup

### 1. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure Gemini

Copy `.env.example` to `.env` and set:

```env
GEMINI_API_KEY=your_api_key_here
```

Optional:

```env
GEMINI_MODEL=gemini-flash-lite-latest
TMDB_READ_ACCESS_TOKEN=your_tmdb_token_here
```

### 4. Run the application

```powershell
python main.py
```

You should see a terminal prompt:

```text
Drama Companion

You:
```

Type `exit` or `quit` to close it.

## Database

SQLite is created automatically at:

```text
data/drama.db
```

You can override it with `DATABASE_URL`.

## Current scope

The project is deliberately CLI-only while the application logic is being
stabilized. A graphical/web interface can be added later without changing the
core database and chatbot logic.
