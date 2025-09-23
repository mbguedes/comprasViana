import psycopg2
from passlib.context import CryptContext
from database import get_db_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def check_user(username, password):
    """Verifica o usuário no banco de dados PostgreSQL."""
    conn = None
    cursor = None
    user_data = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password_hash FROM usuarios WHERE username = %s", (username,))
        user_data = cursor.fetchone()
    except Exception as e:
        print(f"Erro ao checar usuário: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    if user_data:
        user_id = user_data[0]
        hashed_password = user_data[1]
        if verify_password(password, hashed_password):
            return user_id, username
    return None

def add_user(username, password):
    """Adiciona um novo usuário, com tratamento de erro de conexão robusto."""
    if not username or not password:
        return "Usuário e senha não podem estar em branco."
        
    password_hash = get_password_hash(password)
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        conn.commit()
        return "Success"
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        if hasattr(e, 'pgcode') and e.pgcode == '23505': # Código de erro para UNIQUE constraint
            return "Este nome de usuário já existe."
        else:
            print(f"Erro inesperado ao adicionar usuário: {e}")
            return f"Erro inesperado no banco de dados: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()