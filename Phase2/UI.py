import tkinter as tk
from tkinter import messagebox
import CRUD


class NotesApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.current_note_id = None

        self.frame_left = tk.Frame(root, width=200)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        self.listbox = tk.Listbox(self.frame_left)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.incarca_nota)

        self.frame_right = tk.Frame(root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.frame_right, text="Titlu:").pack(anchor="w")
        self.entry_titlu = tk.Entry(self.frame_right)
        self.entry_titlu.pack(fill=tk.X, pady=5)

        tk.Label(self.frame_right, text="Continut:").pack(anchor="w")
        self.text_content = tk.Text(self.frame_right, height=10)
        self.text_content.pack(fill=tk.BOTH, expand=True, pady=5)

        self.btn_save = tk.Button(self.frame_right, text="Salveaza Nota", command=self.salveaza_nota, bg="lightgreen")
        self.btn_save.pack(side=tk.RIGHT)

        self.btn_new = tk.Button(self.frame_left, text="+ Nota Noua", command=self.nota_noua)
        self.btn_new.pack(fill=tk.X)

        self.refresh_lista()

    def refresh_lista(self):
        self.listbox.delete(0, tk.END)
        note = CRUD.get_all_notes_title(self.conn)
        for n in note:
            self.listbox.insert(tk.END, f"{n[0]}: {n[1]}")

    def salveaza_nota(self):
        titlu = self.entry_titlu.get()
        continut = self.text_content.get("1.0", tk.END).strip()

        if not titlu:
            messagebox.showwarning("Eroare", "Pune un titlu!")
            return

        if self.current_note_id is None:
            # Notă nouă (C din CRUD)
            CRUD.create_text_note(self.conn, titlu, continut)
        else:
            # Update (U din CRUD)
            CRUD.update_note_title_content(self.conn, self.current_note_id, titlu, continut)

        self.refresh_lista()
        messagebox.showinfo("Succes", "Nota a fost salvată!")

    def incarca_nota(self, event):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            data = self.listbox.get(index)
            id_nota = int(data.split(":")[0])

            nota = CRUD.get_note_by_id(self.conn, id_nota)
            if nota:
                self.current_note_id = id_nota
                self.entry_titlu.delete(0, tk.END)
                self.entry_titlu.insert(0, nota['title'])
                self.text_content.delete("1.0", tk.END)
                self.text_content.insert("1.0", nota['content'] or "")

    def nota_noua(self):
        self.current_note_id = None
        self.entry_titlu.delete(0, tk.END)
        self.text_content.delete("1.0", tk.END)