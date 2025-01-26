def is_borrowed(title, cur):
    cur.execute("SELECT borrowed FROM book WHERE title = ?", (title,))
    return cur.fetchone()[0]