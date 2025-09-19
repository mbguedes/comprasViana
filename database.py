import streamlit as st
import pandas as pd
from datetime import datetime
import libsql_client
import os

# --- FUNÇÃO DE CONEXÃO CENTRALIZADA ---
# Esta função será a única a se conectar ao banco. Ela usa os segredos do Streamlit.
def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados Turso."""
    url = st.secrets["TURSO_DB_URL"]
    auth_token = st.secrets["TURSO_AUTH_TOKEN"]
    
    # Lógica para garantir que a URL funcione em diferentes ambientes
    if url.startswith("libsql://"):
        url = url.replace("libsql://", "https://")
        
    return libsql_client.create_client_sync(url=url, auth_token=auth_token)

# --- FUNÇÕES DE MANIPULAÇÃO DO BANCO ---
def criar_banco():
    """Verifica e cria as tabelas no banco de dados Turso se não existirem."""
    try:
        conn = get_db_connection()
        # No Turso, é mais eficiente executar múltiplos comandos em um batch
        conn.batch([
            """CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT, data_compra TEXT NOT NULL, nome_produto TEXT NOT NULL,
                fornecedor TEXT, quantidade_comprada REAL NOT NULL, unidade_medida TEXT NOT NULL,
                preco_unitario REAL NOT NULL, numero_nota_fiscal TEXT, id_usuario INTEGER,
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
            );""",
            """CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL
            );""",
            """CREATE TABLE IF NOT EXISTS historico_atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT, id_usuario INTEGER, username TEXT NOT NULL,
                acao TEXT NOT NULL, timestamp TEXT NOT NULL, detalhes TEXT,
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
            );"""
        ])
        conn.close()
        print("Tabelas verificadas/criadas no Turso com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas no Turso: {e}")

def ler_dados_sql():
    """Lê todos os dados da tabela 'compras' do Turso e retorna como um DataFrame."""
    df = pd.DataFrame()
    try:
        conn = get_db_connection()
        query = "SELECT c.*, u.username as registrado_por FROM compras c LEFT JOIN usuarios u ON c.id_usuario = u.id ORDER BY c.data_compra DESC"
        rs = conn.execute(query)
        
        df = pd.DataFrame(rs.rows, columns=rs.columns)
        
        if not df.empty and 'data_compra' in df.columns:
            df['data_compra'] = pd.to_datetime(df['data_compra'])
            
    except Exception as e:
        st.error(f"Erro ao ler dados do banco: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
            
    return df

def salvar_dados_sql(df_compras_para_salvar):
    """Salva um DataFrame de compras no banco de dados Turso."""
    try:
        conn = get_db_connection()
        # Usa uma transação para garantir que todos os inserts sejam bem-sucedidos
        with conn.transaction() as tx:
            for _, row in df_compras_para_salvar.iterrows():
                tx.execute(
                    """
                    INSERT INTO compras (data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal, id_usuario) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (row['data_compra'], row['nome_produto'], row['fornecedor'], row['quantidade_comprada'], row['unidade_medida'], row['preco_unitario'], row['numero_nota_fiscal'], row['id_usuario'])
                )
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados no banco de dados na nuvem: {e}")
        return False
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def registrar_log(id_usuario, username, acao, detalhes=""):
    """Insere um novo registro na tabela de histórico de atividades no Turso."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn = get_db_connection()
        conn.execute(
            """INSERT INTO historico_atividades (id_usuario, username, acao, timestamp, detalhes) VALUES (?, ?, ?, ?, ?)""",
            (id_usuario, username, acao, timestamp, detalhes)
        )
    except Exception as e:
        st.error(f"Erro ao registrar log: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

# O bloco if __name__ == '__main__' pode ser mantido para testes locais se necessário
if __name__ == '__main__':
    # Para rodar este script, você precisaria configurar os segredos localmente
    # print("Este script agora depende dos segredos do Streamlit para conectar ao banco.")
    pass