import sqlite3
#scriptul de creare a bazei de date
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT, 
    type TEXT NOT NULL 
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS checklist_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    checked INTEGER DEFAULT 0,
    note_id INTEGER NOT NULL,
    FOREIGN KEY (note_id) REFERENCES notes(id) ON DELETE CASCADE
)
""")
conn.commit()
conn.close()