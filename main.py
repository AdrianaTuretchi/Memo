import sqlite3
from CRUD import get_all_notes, update_note_title_content, delete_note_by_id

try:
    with sqlite3.connect('notes.db') as conn:
        cursor = conn.cursor()
        update_note_title_content(conn, "1","Nou","content nou")
        delete_note_by_id(conn, "1")
        print(get_all_notes(conn))
except sqlite3.Error as e:
    print(f"O eroare DB a oprit tranzacția: {e}")





