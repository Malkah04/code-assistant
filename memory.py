import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "conversation_memory.sqlite3"

def init_memory():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_message TEXT NOT NULL,
                intent TEXT,
                assistant_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_interaction(user_message, intent, assistant_response):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO conversations
            (user_message, intent, assistant_response)
            VALUES (?, ?, ?)
            """,
            (user_message, intent, assistant_response),
        )

def get_last_k_message(k=5):
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT user_message, intent, assistant_response
            FROM conversations
            ORDER BY id DESC
            LIMIT ?
            """,
            (k,),
        ).fetchall()

    if not rows:
        return "No previous conversation."

    rows.reverse()
    memory_parts = []

    for user_message, intent, assistant_response in rows:
        memory_parts.append(
            f"User: {user_message}\n"
            f"Intent: {intent}\n"
            f"Assistant: {assistant_response}"
        )

    return "\n\n".join(memory_parts)


    
