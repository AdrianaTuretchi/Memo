import tkinter as tk
from tkinter import messagebox
import CRUD


class NotesApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.current_note_id = None
        self.current_type = None
        self.checklist_widgets = []

        self.setup_ui()
        self.ascunde_editorul()
        self.refresh_lista()

    def setup_ui(self):
        # --- Panou Stânga ---
        self.frame_left = tk.Frame(self.root, width=200, bg="#f0f0f0")
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        tk.Label(self.frame_left, text="Notele Mele", bg="#f0f0f0", font=("Arial", 10, "bold")).pack(pady=5)

        self.listbox = tk.Listbox(self.frame_left, font=("Arial", 10))
        self.listbox.pack(fill=tk.BOTH, expand=True, pady=5)
        self.listbox.bind('<<ListboxSelect>>', self.incarca_nota)

        tk.Button(self.frame_left, text="+ Text Note", command=lambda: self.pregateste_nota('text')).pack(fill=tk.X)
        tk.Button(self.frame_left, text="+ Checklist", command=lambda: self.pregateste_nota('checklist')).pack(
            fill=tk.X, pady=2)

        self.btn_delete = tk.Button(self.frame_left, text="Șterge Nota", fg="red", command=self.sterge_nota_total)
        self.btn_delete.pack(fill=tk.X, pady=10)

        # --- Panou Dreapta ---
        self.frame_right = tk.Frame(self.root)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.lbl_titlu = tk.Label(self.frame_right, text="Titlu:")
        self.entry_titlu = tk.Entry(self.frame_right, font=("Arial", 12))

        self.container_editor = tk.Frame(self.frame_right)
        self.container_editor.pack(fill=tk.BOTH, expand=True)

        self.text_editor = tk.Text(self.container_editor, font=("Arial", 11), height=10)
        self.checklist_frame = tk.Frame(self.container_editor)

        self.btn_add_row = tk.Button(self.frame_right, text="+ Adaugă rând",
                                     command=lambda: self.add_blank_checklist_row())
        self.btn_save = tk.Button(self.frame_right, text="Salvează Nota", bg="#4CAF50", fg="white",
                                  font=("Arial", 10, "bold"), command=self.salveaza_nota)

    def ascunde_editorul(self):
        self.lbl_titlu.pack_forget()
        self.entry_titlu.pack_forget()
        self.text_editor.pack_forget()
        self.checklist_frame.pack_forget()
        self.btn_add_row.pack_forget()
        self.btn_save.pack_forget()

    def afiseaza_editorul(self, tip):
        self.lbl_titlu.pack(anchor="w")
        self.entry_titlu.pack(fill=tk.X, pady=5)
        if tip == 'text':
            self.text_editor.pack(fill=tk.BOTH, expand=True)
        else:
            self.checklist_frame.pack(fill=tk.BOTH, expand=True)
            self.btn_add_row.pack(pady=5)
        self.btn_save.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

    def refresh_lista(self):
        self.listbox.delete(0, tk.END)
        note = CRUD.get_all_notes_title(self.conn)
        for n in note:
            self.listbox.insert(tk.END, f"{n[0]}: {n[1]}")

    def incarca_nota(self, event):
        selection = self.listbox.curselection()
        if not selection: return

        try:
            item_text = self.listbox.get(selection[0])
            id_nota = int(item_text.split(":")[0])

            nota = CRUD.get_note_by_id(self.conn, id_nota)
            if not nota: return

            self.current_note_id = id_nota
            self.current_type = nota['type']
            self.ascunde_editorul()
            self.afiseaza_editorul(self.current_type)

            self.entry_titlu.delete(0, tk.END)
            self.entry_titlu.insert(0, nota['title'])

            if nota['type'] == 'text':
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", nota['content'] or "")
            else:
                self.curata_interfata_checklist()
                for item in nota.get('checklist_items', []):
                    self.add_blank_checklist_row(item['content'], item['checked'], item['id'])
            print(f"DEBUG: Încărcat nota ID {self.current_note_id}")
        except Exception as e:
            print(f"Eroare la încărcare: {e}")

    def pregateste_nota(self, tip):
        self.current_note_id = None  # RESETĂM ID-ul pentru a evita copiile
        self.current_type = tip
        self.ascunde_editorul()
        self.afiseaza_editorul(tip)
        self.entry_titlu.delete(0, tk.END)
        self.curata_interfata_checklist()
        if tip == 'text':
            self.text_editor.delete("1.0", tk.END)
        else:
            self.add_blank_checklist_row()

    def curata_interfata_checklist(self):
        for w in self.checklist_widgets:
            w['frame'].destroy()
        self.checklist_widgets = []

    def add_blank_checklist_row(self, content="", checked=False, item_id=None):
        row = tk.Frame(self.checklist_frame)
        row.pack(fill=tk.X, pady=2)
        var = tk.BooleanVar(value=checked)
        chk = tk.Checkbutton(row, variable=var)
        chk.pack(side=tk.LEFT)
        ent = tk.Entry(row)
        ent.insert(0, content)
        ent.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        btn_del = tk.Button(row, text="✕", fg="red", bd=0,
                            command=lambda r=row, i=item_id: self.sterge_item_checklist(r, i))
        btn_del.pack(side=tk.RIGHT)
        self.checklist_widgets.append({'frame': row, 'var': var, 'entry': ent, 'id': item_id})

    def sterge_item_checklist(self, frame, item_id):
        if item_id:
            CRUD.delete_checklist_item(self.conn, item_id)
        frame.destroy()
        self.checklist_widgets = [w for w in self.checklist_widgets if w['frame'] != frame]

    def salveaza_nota(self):
        try:
            titlu = self.entry_titlu.get().strip()
            if not titlu:
                messagebox.showwarning("Eroare", "Titlul este obligatoriu!")
                return

            # --- LOGICĂ TEXT NOTE ---
            if self.current_type == 'text':
                continut = self.text_editor.get("1.0", tk.END).strip()
                if self.current_note_id:
                    CRUD.update_note_title_content(self.conn, self.current_note_id, titlu, continut)
                else:
                    self.current_note_id = CRUD.create_text_note(self.conn, titlu, continut)

            # --- LOGICĂ CHECKLIST ---
            elif self.current_type == 'checklist':
                if not self.current_note_id:
                    # Notă complet nouă
                    items = [w['entry'].get() for w in self.checklist_widgets if w['entry'].get().strip()]
                    self.current_note_id = CRUD.create_checklist_note(self.conn, titlu, items)
                else:
                    # Update Notă existentă
                    CRUD.update_note_title_content(self.conn, self.current_note_id, titlu, None)

                    for w in self.checklist_widgets:
                        text_item = w['entry'].get().strip()
                        status_bifa = 1 if w['var'].get() else 0

                        if not text_item: continue  # Sărim peste rândurile goale

                        if w['id']:
                            # Itemul există deja -> UPDATE
                            CRUD.update_checklist_item_text(self.conn, w['id'], text_item)
                            CRUD.update_checked_status(self.conn, w['id'], status_bifa)
                        else:
                            # Itemul este proaspăt adăugat cu butonul "+ Adaugă rând" -> INSERT
                            noul_id = CRUD.update_checked_note(self.conn, self.current_note_id, text_item)
                            w['id'] = noul_id  # Îi atribuim ID-ul primit ca să nu îl mai insereze a doua oară

            self.refresh_lista()
            messagebox.showinfo("Succes", "Nota a fost actualizată cu succes!")

        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la salvare: {e}")
    def sterge_nota_total(self):
        if self.current_note_id is None:
            messagebox.showwarning("Atenție", "Selectează o notă din listă pentru a o șterge!")
            return

        if messagebox.askyesno("Confirmare", f"Sigur ștergi definitiv nota {self.current_note_id}?"):
            if CRUD.delete_note_by_id(self.conn, self.current_note_id):
                self.current_note_id = None
                self.ascunde_editorul()
                self.refresh_lista()
                messagebox.showinfo("Succes", "Nota a fost ștearsă!")
            else:
                messagebox.showerror("Eroare", "Ștergerea a eșuat.")