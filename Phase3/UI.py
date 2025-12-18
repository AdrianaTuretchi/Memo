import tkinter as tk
from tkinter import messagebox
import CRUD

class NotesApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.current_note_id = None
        self.checklist_widgets = []

        self.setup_ui()
        self.refresh_lista()

    def setup_ui(self):
        self.frame_left = tk.Frame(self.root, width=200, bg="#e0e0e0")
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        self.listbox = tk.Listbox(self.frame_left)
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.incarca_nota)

        tk.Button(self.frame_left, text="+ Text Note", command=lambda: self.pregateste_nota('text')).pack(fill=tk.X)
        tk.Button(self.frame_left, text="+ Checklist", command=lambda: self.pregateste_nota('checklist')).pack(
            fill=tk.X, pady=2)

        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(self.frame_right, text="Titlu:").pack(anchor="w")
        self.entry_titlu = tk.Entry(self.frame_right, font=("Arial", 12))
        self.entry_titlu.pack(fill=tk.X, pady=5)

        self.container_continut = tk.Frame(self.frame_right)
        self.container_continut.pack(fill=tk.BOTH, expand=True)


        self.text_editor = tk.Text(self.container_continut, height=10)

        self.checklist_frame = tk.Frame(self.container_continut)
        self.btn_add_item = tk.Button(self.frame_right, text="+ Adaugă rând", command=self.add_blank_checklist_row)

        self.btn_save = tk.Button(self.frame_right, text="Salvează Tot", command=self.salveaza_nota, bg="#4CAF50",
                                  fg="white")
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def pregateste_nota(self, tip):
        self.current_note_id = None
        self.current_type = tip
        self.entry_titlu.delete(0, tk.END)
        self.curata_interfata_editor()

        if tip == 'text':
            self.text_editor.pack(fill=tk.BOTH, expand=True)
            self.text_editor.delete("1.0", tk.END)
            self.btn_add_item.pack_forget()
        else:
            self.checklist_frame.pack(fill=tk.BOTH, expand=True)
            self.btn_add_item.pack(pady=5)
            self.add_blank_checklist_row()

    def curata_interfata_editor(self):
        self.text_editor.pack_forget()
        self.checklist_frame.pack_forget()
        for widget in self.checklist_widgets:
            widget['frame'].destroy()
        self.checklist_widgets = []

    def add_blank_checklist_row(self, content="", checked=False, item_id=None):
        row_frame = tk.Frame(self.checklist_frame)
        row_frame.pack(fill=tk.X, pady=2)

        var = tk.BooleanVar(value=checked)
        chk = tk.Checkbutton(row_frame, variable=var)
        chk.pack(side=tk.LEFT)

        ent = tk.Entry(row_frame)
        ent.insert(0, content)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True)

        btn_del = tk.Button(row_frame, text="X", fg="red", command=lambda: self.remove_row(row_frame, item_id))
        btn_del.pack(side=tk.RIGHT)

        self.checklist_widgets.append({'frame': row_frame, 'var': var, 'entry': ent, 'id': item_id})

    def remove_row(self, frame, item_id):
        frame.destroy()
        self.checklist_widgets = [w for w in self.checklist_widgets if w['frame'] != frame]

    def salveaza_nota(self):
        titlu = self.entry_titlu.get()
        if not titlu: return

        if self.current_type == 'text':
            continut = self.text_editor.get("1.0", tk.END).strip()
            if self.current_note_id:
                CRUD.update_note_title_content(self.conn, self.current_note_id, titlu, continut)
            else:
                CRUD.create_text_note(self.conn, titlu, continut)

        elif self.current_type == 'checklist':
            items = [w['entry'].get() for w in self.checklist_widgets if w['entry'].get().strip() != ""]
            if not self.current_note_id:
                self.current_note_id = CRUD.create_checklist_note(self.conn, titlu, items)
            else:
                CRUD.update_note_title_content(self.conn, self.current_note_id, titlu, None)
            for w in self.checklist_widgets:
                if w['id']:
                    CRUD.update_checked_status(self.conn, w['id'], 1 if w['var'].get() else 0)

        self.refresh_lista()
        messagebox.showinfo("Succes", "Salvat!")

    def incarca_nota(self, event):
        selection = self.listbox.curselection()
        if not selection: return

        id_nota = int(self.listbox.get(selection[0]).split(":")[0])
        nota = CRUD.get_note_by_id(self.conn, id_nota)

        self.current_note_id = id_nota
        self.current_type = nota['type']
        self.curata_interfata_editor()

        self.entry_titlu.delete(0, tk.END)
        self.entry_titlu.insert(0, nota['title'])

        if nota['type'] == 'text':
            self.text_editor.pack(fill=tk.BOTH, expand=True)
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", nota['content'] or "")
            self.btn_add_item.pack_forget()
        else:
            self.checklist_frame.pack(fill=tk.BOTH, expand=True)
            self.btn_add_item.pack(pady=5)
            for item in nota.get('checklist_items', []):
                self.add_blank_checklist_row(item['content'], item['checked'], item['id'])

    def refresh_lista(self):
        self.listbox.delete(0, tk.END)
        for n in CRUD.get_all_notes_title(self.conn):
            self.listbox.insert(tk.END, f"{n[0]}: {n[1]}")