import sqlite3
from passlib.context import CryptContext

DB_NAME = 'dados/viana.db'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def check_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, password_hash FROM usuarios WHERE username = ?", (username,))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        user_id = user_data[0]
        hashed_password = user_data[1]
        if verify_password(password, hashed_password):
            return user_id, username
        return None
    
    

def add_user(username, password):
    password_hash = get_password_hash(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()