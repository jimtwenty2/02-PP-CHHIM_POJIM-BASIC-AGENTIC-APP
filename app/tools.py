from app.database import get_connection

def list_books():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, author, copies FROM books ORDER BY id"
        ).fetchall()

    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "copies": row[3],
        })

    return {"ok": True, "books": books}

def search_book(query):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, author FROM books WHERE title ILIKE %s ORDER BY id",
            (f"%{query}%",),
        ).fetchall()

    books = []
    for row in rows:
        books.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
        })

    return {
        "ok": True,
        "books": books,
    }

def check_availability(book_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT copies FROM books WHERE id = %s",
            (book_id,),
        ).fetchone()

    if not row:
        return {"ok": False, "error": "BOOK_NOT_FOUND"}

    return {"ok": True, "book_id": book_id, "copies": row[0]}


def borrow_book(book_id):
    with get_connection() as conn:
        # copies only if copies > 0
        row = conn.execute(
            """
            UPDATE books SET copies = copies - 1
            WHERE id = %s AND copies > 0
            RETURNING copies
            """,
            (book_id,),
        ).fetchone()

        if not row:
            exists = conn.execute(
                "SELECT 1 FROM books WHERE id = %s",
                (book_id,),
            ).fetchone()

            if not exists:
                return {"ok": False, "error": "BOOK_NOT_FOUND"}
            return {"ok": False, "error": "OUT_OF_STOCK"}

        conn.execute(
            "INSERT INTO borrow_log (book_id) VALUES (%s)",
            (book_id,),
        )

        return {"ok": True, "book_id": book_id, "copies_left": row[0]}