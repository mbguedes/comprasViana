import sqlite3
import os

DB_NAME = 'dados/viana.db'

def criar_banco():
    """Cria e conecta ao banco de dados, e cria a tabela 'compras' se ela não existir."""
    
    os.makedirs('dados', exist_ok=True)
    
    conn = sqlite3.connect(DB_NAME)
    
    cursor = conn.cursor()
    
    print("Conectado ao banco de dados SQLite.")
    
    sql_command = """
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_compra TEXT NOT NULL,
        nome_produto TEXT NOT NULL,
        fornecedor TEXT,
        quantidade_comprada REAL NOT NULL,
        unidade_medida TEXT NOT NULL,
        preco_unitario REAL NOT NULL,
        numero_nota_fiscal TEXT
    );
    """
    
    cursor.execute(sql_command)
    
    print("Tabela 'compras' verificada/criada com sucesso.")
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco()