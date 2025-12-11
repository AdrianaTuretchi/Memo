import sqlite3
#conn = sqlite3.connect("notes.db")
#cursor = conn.cursor()

    #C
def create_text_note(conn,title, content):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, content, type) VALUES (?, ?, 'text')", (title, content))
    conn.commit()
    return cursor.lastrowid

def create_checklist_note(conn,title, items):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (title, type) VALUES (?, 'checklist')", (title,))
    note_id = cursor.lastrowid
    item_data = [(item, note_id) for item in items]
    cursor.executemany("INSERT INTO checklist_items (content, note_id) VALUES (?, ?)", item_data)
    conn.commit()
    return note_id

# R
def get_note_by_title(conn,note_title):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE title  = ?", (note_title,))
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
        cursor.execute("SELECT id, content, checked FROM checklist_items WHERE note_id = ?", (note_title,))
        result["checklist_items"] = [{"id": item[0], "content": item[1], "checked": bool(item[2])} for item in
                                     cursor.fetchall()]
    return result

def get_note_by_id(conn,note_id):
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
        result["checklist_items"] = [{"id": item[0], "content": item[1], "checked": bool(item[2])} for item in
                                     cursor.fetchall()]
    return result

def get_all_notes(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    all_notes = cursor.fetchall()
    return all_notes

#U



def update_note_title_content(conn,note_id, new_title=None, new_content=None):
    set_clauses = []
    params = []
    if new_title is not None:
        if new_title.strip() == "":
            print("Eroare: Titlul nu poate fi gol.")
            return False
        set_clauses.append("title = ?")
        params.append(new_title)
    if new_content is not None:
        set_clauses.append("content = ?")
        params.append(new_content)
    if not set_clauses:
        print("Avertisment: Nu au fost furnizate titlu sau conținut nou.")
        return False
    set_query = ", ".join(set_clauses)
    sql_query = f"UPDATE notes SET {set_query} WHERE id = ?"
    params.append(note_id)
    cursor = conn.cursor()
    cursor.execute(sql_query, tuple(params))
    return True

#D
def delete_note_by_id(conn,note_id):
    cursor = conn.cursor()
    sql_query = "DELETE FROM notes WHERE id = ?"
    cursor.execute(sql_query, (note_id,))
    if cursor.rowcount > 0:
        return True
    else:
        return False
