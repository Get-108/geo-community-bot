import sqlite3

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER UNIQUE,
        name TEXT,
        country TEXT,
        city TEXT,
        token TEXT
    )""")
    conn.commit()
    conn.close()

def save_user(telegram_id, name, country, city, token):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (telegram_id, name, country, city, token) VALUES (?, ?, ?, ?, ?)",
              (telegram_id, name, country, city, token))
    conn.commit()
    conn.close()

def get_user_by_token(token):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE token=?", (token,))
    user = c.fetchone()
    conn.close()
    return user

def get_all_users():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT name, country, city FROM users")
    users = [{"name": row[0], "country": row[1], "city": row[2]} for row in c.fetchall()]
    conn.close()
    return users
