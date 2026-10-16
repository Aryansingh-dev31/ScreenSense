import os
import sqlite3
from datetime import datetime

import pyautogui
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from screen_selector import select_area
from google import genai
from google.genai import types
from google.genai.errors import ClientError

load_dotenv(dotenv_path=".env")

import threading
import keyboard  # add to imports at the top

# ... keep everything you already have ...

def hotkey_capture():
    """Runs in the background, fires on Ctrl+Shift+S from anywhere."""
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO sessions (image_path, created_at) VALUES (?, ?)",
        ("", datetime.utcnow().isoformat()),
    )
    session_id = cur.lastrowid

    filename = f"{session_id}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshots/{filename}")

    conn.execute("UPDATE sessions SET image_path = ? WHERE id = ?", (filename, session_id))
    conn.commit()
    conn.close()

    print(f"📸 Hotkey capture saved as session {session_id}")


def start_hotkey_listener():
    keyboard.add_hotkey("ctrl+shift+x", hotkey_capture)
    keyboard.wait()  # blocks this thread forever, listening


# Start the listener in a background thread when the app boots
threading.Thread(target=start_hotkey_listener, daemon=True).start()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("screenshots", exist_ok=True)
app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")

DB_PATH = "screensense.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            role TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        )
    """)
    conn.commit()
    conn.close()


init_db()


class Question(BaseModel):
    question: str
    session_id: int


@app.post("/capture")
def capture_screen():
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO sessions (image_path, created_at) VALUES (?, ?)",
        ("", datetime.utcnow().isoformat()),
    )
    session_id = cur.lastrowid

    filename = f"{session_id}.png"
    screenshot = pyautogui.screenshot()
    screenshot.save(f"screenshots/{filename}")

    conn.execute("UPDATE sessions SET image_path = ? WHERE id = ?", (filename, session_id))
    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "image": f"http://127.0.0.1:8000/screenshots/{filename}",
    }


@app.post("/select-area")
def select_screen_area():
    selected_path = select_area()

    if not selected_path:
        return {"error": "No area selected"}

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO sessions (image_path, created_at) VALUES (?, ?)",
        ("", datetime.utcnow().isoformat()),
    )
    session_id = cur.lastrowid

    filename = f"{session_id}.png"
    os.replace(selected_path, f"screenshots/{filename}")

    conn.execute("UPDATE sessions SET image_path = ? WHERE id = ?", (filename, session_id))
    conn.commit()
    conn.close()

    return {
        "session_id": session_id,
        "image": f"http://127.0.0.1:8000/screenshots/{filename}",
    }


@app.get("/sessions")
def list_sessions():
    conn = get_db()
    sessions = conn.execute("SELECT * FROM sessions ORDER BY id DESC").fetchall()

    result = []
    for s in sessions:
        messages = conn.execute(
            "SELECT role, text FROM messages WHERE session_id = ? ORDER BY id ASC",
            (s["id"],),
        ).fetchall()
        result.append({
            "id": s["id"],
            "image": f"http://127.0.0.1:8000/screenshots/{s['image_path']}",
            "created_at": s["created_at"],
            "messages": [{"role": m["role"], "text": m["text"]} for m in messages],
        })

    conn.close()
    return result

@app.delete("/sessions")
def delete_history():
    conn = get_db()

    conn.execute("DELETE FROM messages")
    conn.execute("DELETE FROM sessions")
    conn.commit()
    conn.close()

    return {"message": "History deleted successfully"}

@app.post("/ask")
def ask_screen(question: Question):
    conn = get_db()

    session = conn.execute(
        "SELECT * FROM sessions WHERE id = ?", (question.session_id,)
    ).fetchone()
    if not session:
        conn.close()
        return {"answer": "⚠️ Session not found."}

    prior_messages = conn.execute(
        "SELECT role, text FROM messages WHERE session_id = ? ORDER BY id ASC",
        (question.session_id,),
    ).fetchall()

    image_path = f"screenshots/{session['image_path']}"
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    contents = [
        types.Content(role=m["role"], parts=[types.Part.from_text(text=m["text"])])
        for m in prior_messages
    ]
    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question.question),
                types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
            ],
        )
    )

    now = datetime.utcnow().isoformat()
    conn.execute(
        "INSERT INTO messages (session_id, role, text, created_at) VALUES (?, ?, ?, ?)",
        (question.session_id, "user", question.question, now),
    )
    conn.commit()

    try:
        response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=contents,
        )
        answer = response.text
    except ClientError as e:
        answer = (
            "⚠️ Rate limit hit — please wait a minute and try again."
            if e.status_code == 429
            else f"⚠️ API error: {e.message}"
        )

    conn.execute(
        "INSERT INTO messages (session_id, role, text, created_at) VALUES (?, ?, ?, ?)",
        (question.session_id, "model", answer, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()

    return {"answer": answer}