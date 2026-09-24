from app.database import get_connection

def create_tables():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                author VARCHAR(255) NOT NULL,
                published_year INTEGER,
                copies INTEGER NOT NULL DEFAULT 0 CHECK (copies >= 0),
                UNIQUE (title, author)
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS borrow_log (
                id SERIAL PRIMARY KEY,
                book_id INTEGER NOT NULL REFERENCES books(id),
                borrowed_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
        """)
    print("Tables created successfully.")


def seed_books():
    with get_connection() as conn:
        # ON CONFLICT DO NOTHING: running this again adds no duplicates
        conn.execute("""
            INSERT INTO books (title, author, published_year, copies)
            VALUES
                ('Sophat', 'Rim Kin', 1938, 30),
                ('Kolab Pailin', 'Nou Hach', 1943, 10),
                ('Phka Srapoun', 'Nou Hach', 1947, 5),
                ('Tum Teav', 'Preah Botumthera Som', 1915, 15),
                ('Reamker', 'Anonymous', 1600, 0)
            ON CONFLICT (title, author) DO NOTHING;
        """)
    print("Seed data inserted successfully.")

# In case, we want to reset data
def reset_data():
    """Empty both tables, restart ids from 1, and seed again."""
    with get_connection() as conn:
        conn.execute("TRUNCATE borrow_log, books RESTART IDENTITY CASCADE;")
    seed_books()


if __name__ == "__main__":
    create_tables()
    seed_books()