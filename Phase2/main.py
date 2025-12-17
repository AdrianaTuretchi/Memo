<<<<<<< HEAD
import sqlite3
import tkinter as tk
from UI import NotesApp

def main():
    conn = sqlite3.connect("notes.db")
    root = tk.Tk()
    root.title("Aplicația mea de Note")
    root.geometry("600x400")
    app = NotesApp(root, conn)
    root.mainloop()
    conn.close()

if __name__ == "__main__":
    main()
=======
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





>>>>>>> 0ed25b50bdc9f3d6eb1c92c243dd046c55582d16
