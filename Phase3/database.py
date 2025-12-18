<<<<<<< HEAD
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
=======
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
>>>>>>> 0ed25b50bdc9f3d6eb1c92c243dd046c55582d16
conn.close()