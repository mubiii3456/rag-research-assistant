import sqlite3
import os
from datetime import datetime
 
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "chat_history.db")
 
 
def get_connection():
    return sqlite3.connect(DB_PATH)
 
 
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
 
 
def save_message(session_id: str, user_id: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_messages (session_id, user_id, role, content, timestamp) VALUES (?, ?, ?, ?, ?)",
        (session_id, user_id, role, content, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()
 
 
def load_messages(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content FROM chat_messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,),
    )
    rows = cursor.fetchall()
    conn.close()
    return [{"role": role, "content": content} for role, content in rows]
 
 
def clear_session_messages(session_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def get_all_sessions(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT session_id, content, timestamp
        FROM chat_messages
        WHERE role = 'user' AND user_id = ?
        ORDER BY timestamp ASC
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    sessions = {}
    for session_id, content, timestamp in rows:
        if session_id not in sessions:
            sessions[session_id] = {"session_id": session_id, "title": content[:40], "first_time": timestamp}

    ordered = sorted(sessions.values(), key=lambda s: s["first_time"], reverse=True)
    return ordered
if __name__ == "__main__":
    init_db()
    print(f"Database initialized at: {DB_PATH}")