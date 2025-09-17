import sqlite3
import os
import pandas as pd

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
    conn.commit()
    conn.close()
    print("Banco de Dados e tabela verificada/criada com sucesso.")
 

def ler_dados_sql():
    """Lê todos os dados da tabela 'compras' e retorna como um DataFrame."""
    if not os.path.exists(DB_NAME):
        return pd.DataFrame() # Retorna um DataFrame vazio se não houver banco

    try:
        conn = sqlite3.connect(DB_NAME)
        query = "SELECT * FROM compras ORDER BY data_compra DESC"
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Converte a coluna de data para o tipo datetime para melhor manipulação
        if not df.empty:
            df['data_compra'] = pd.to_datetime(df['data_compra'])
        
        return df
    except Exception as e:
        print(f"Erro ao ler dados: {e}")
        return pd.DataFrame()
    

if __name__ == '__main__':
    criar_banco()