import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_NAME = 'dados/viana.db'

def criar_banco():
    """Cria e conecta ao banco de dados, e cria as tabelas necessárias se não existirem."""
    os.makedirs('dados', exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    print("Conectado ao banco de dados SQLite.")
    
    sql_compras = """
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_compra TEXT NOT NULL,
        nome_produto TEXT NOT NULL,
        fornecedor TEXT,
        quantidade_comprada REAL NOT NULL,
        unidade_medida TEXT NOT NULL,
        preco_unitario REAL NOT NULL,
        numero_nota_fiscal TEXT,
        id_usuario INTEGER,
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
    );
    """
    
    sql_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """
    

    sql_historico = """
    CREATE TABLE IF NOT EXISTS historico_atividades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario INTEGER,
        username TEXT NOT NULL,
        acao TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        detalhes TEXT,
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
    );
    """
    
    cursor.execute(sql_compras)
    cursor.execute(sql_usuarios)
    cursor.execute(sql_historico) 
    
    conn.commit()
    conn.close()
    print("Banco de Dados e tabelas verificados/criados com sucesso.")


def ler_dados_sql():
    """Lê todos os dados da tabela 'compras' e retorna como um DataFrame."""
    if not os.path.exists(DB_NAME):
        return pd.DataFrame()

    try:
        conn = sqlite3.connect(DB_NAME)
        query = """
            SELECT c.*, u.username as registrado_por
            FROM compras c
            LEFT JOIN usuarios u ON c.id_usuario = u.id
            ORDER BY c.data_compra DESC
        """

        df = pd.read_sql_query(query, conn)
        conn.close()
        
        if not df.empty:
            df['data_compra'] = pd.to_datetime(df['data_compra'])
        
        return df
    except Exception as e:
        print(f"Erro ao ler dados: {e}")
        return pd.DataFrame()

#FuncLog
def registrar_log(id_usuario, username, acao, detalhes=""):
    """Insere um novo registro na tabela de histórico de atividades."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
        INSERT INTO historico_atividades (id_usuario, username, acao, timestamp, detalhes)
        VALUES (?, ?, ?, ?, ?)
    """, (id_usuario, username, acao, timestamp, detalhes))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco()