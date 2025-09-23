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
    """Adiciona um novo usuário, retornando uma mensagem de sucesso ou o erro específico."""
    if not username or not password:
        return "Usuário e senha não podem estar em branco."
        
    password_hash = get_password_hash(password)
    conn = None
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO usuarios (username, password_hash) VALUES (?, ?)", (username, password_hash))
        return "Success"
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            return "Este nome de usuário já existe."
        else:
            print(f"Erro inesperado ao adicionar usuário: {e}")
            return f"Erro inesperado no banco de dados: {e}"
    finally:
        if conn:
            conn.close()