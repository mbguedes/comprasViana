from passlib.context import CryptContext
from database import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def check_user(username, password):
    """Verifica o usuário no banco de dados Turso."""
    conn = None
    user_data = None
    try:
        conn = get_db_connection()
        rs = conn.execute("SELECT id, password_hash FROM usuarios WHERE username = ?", (username,))
        if rs.rows:
            user_data = rs.rows[0]
    except Exception as e:
        print(f"Erro ao checar usuário: {e}")
    finally:
        if conn:
            conn.close()

    if user_data:
        user_id = user_data[0]
        hashed_password = user_data[1]
        if verify_password(password, hashed_password):
            return user_id, username
    return None

def add_user(username, password):
    """Adiciona um novo usuário no banco de dados Turso, garantindo o commit."""
    password_hash = get_password_hash(password)
    conn = None
    try:
        conn = get_db_connection()
        # Envolve a criação do usuário em uma transação para garantir o commit
        with conn.transaction() as tx:
            tx.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, password_hash))
        return True
    except Exception as e:
        print(f"Erro ao adicionar usuário: {e}")
        return False
    finally:
        if conn:
            conn.close()