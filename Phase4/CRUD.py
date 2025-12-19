import sqlite3
# --- CREATE ---
def create_text_note(conn, title, content):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, content, type) VALUES (?, ?, 'text')", (title, content))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Eroare la crearea notei text: {e}")
        return None

def create_checklist_note(conn, title, items):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes (title, type) VALUES (?, 'checklist')", (title,))
        note_id = cursor.lastrowid
        item_data = [(item, note_id) for item in items]
        cursor.executemany("INSERT INTO checklist_items (content, note_id) VALUES (?, ?)", item_data)
        conn.commit()
        return note_id
    except sqlite3.Error as e:
        print(f"Eroare la crearea checklist-ului: {e}")
        conn.rollback()
        return None
# --- READ ---

def get_note_by_id(conn, note_id):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        note = cursor.fetchone()
        if not note:
            return None

        result = {
            "id": note[0],
            "title": note[1],
            "content": note[2],
            "type": note[3]
        }

        if result["type"] == 'checklist':
            cursor.execute("SELECT id, content, checked FROM checklist_items WHERE note_id = ?", (note_id,))
            result["checklist_items"] = [
                {"id": item[0], "content": item[1], "checked": bool(item[2])}
                for item in cursor.fetchall()
            ]
        return result
    except sqlite3.Error as e:
        print(f"Eroare la citirea notei: {e}")
        return None


def get_all_notes_title(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM notes")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Eroare la preluarea listei: {e}")
        return []

# --- UPDATE ---

def update_checked_status(conn, item_id, checked):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE checklist_items SET checked = ? WHERE id = ?", (int(checked), item_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Eroare la actualizarea statusului bifat: {e}")

def update_note_title_content(conn, note_id, new_title=None, new_content=None):
    try:
        set_clauses = []
        params = []
        if new_title is not None:
            if new_title.strip() == "": return False
            set_clauses.append("title = ?")
            params.append(new_title)
        if new_content is not None:
            set_clauses.append("content = ?")
            params.append(new_content)

        if not set_clauses: return False

        sql_query = f"UPDATE notes SET {', '.join(set_clauses)} WHERE id = ?"
        params.append(note_id)

        cursor = conn.cursor()
        cursor.execute(sql_query, tuple(params))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Eroare la update: {e}")
        return False
def update_checked_note(conn, note_id, content):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO checklist_items (content, note_id, checked) VALUES (?, ?, 0)", (content, note_id))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Eroare la inserare item nou: {e}")
        return None

def update_checklist_item_text(conn, item_id, new_content):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE checklist_items SET content = ? WHERE id = ?", (new_content, item_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Eroare update text item: {e}")

# --- DELETE ---

def delete_note_by_id(conn, note_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checklist_items WHERE note_id = ?", (note_id,))
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Eroare la ștergerea notei: {e}")
        conn.rollback()
        return False

def delete_checklist_item(conn, item_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM checklist_items WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Eroare la ștergerea item-ului: {e}")
        return False