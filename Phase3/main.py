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