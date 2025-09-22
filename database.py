import streamlit as st
import pandas as pd
from datetime import datetime
import libsql_client
import os

# --- FUNÇÃO DE CONEXÃO CENTRALIZADA ---
def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados Turso."""
    url = st.secrets["TURSO_DB_URL"]
    auth_token = st.secrets["TURSO_AUTH_TOKEN"]
    
    if url.startswith("libsql://"):
        url = url.replace("libsql://", "https://")
        
    return libsql_client.create_client_sync(url=url, auth_token=auth_token)

# --- FUNÇÕES DE MANIPULAÇÃO DO BANCO ---
def criar_banco():
    """Verifica e cria as tabelas no banco de dados Turso se não existirem."""
    conn = None
    try:
        conn = get_db_connection()
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
        print("Tabelas verificadas/criadas no Turso com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas no Turso: {e}")
    finally:
        if conn:
            conn.close()

def ler_dados_sql():
    """Lê todos os dados da tabela 'compras' do Turso e retorna como um DataFrame."""
    conn = None
    try:
        conn = get_db_connection()
        query = "SELECT c.*, u.username as registrado_por FROM compras c LEFT JOIN usuarios u ON c.id_usuario = u.id ORDER BY c.data_compra DESC"
        rs = conn.execute(query)
        
        df = pd.DataFrame(rs.rows, columns=rs.columns)
        
        if not df.empty and 'data_compra' in df.columns:
            df['data_compra'] = pd.to_datetime(df['data_compra'])

        return df # <<< CORREÇÃO AQUI
            
    except Exception as e:
        st.error(f"Erro ao ler dados do banco: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# Em database.py

def salvar_dados_sql(df_compras_para_salvar): # Mantemos os argumentos para não quebrar a chamada
    """Tenta inserir UMA ÚNICA LINHA de dados fixos para teste."""
    
    print("\n--- [DEBUG] INICIANDO TESTE DE INSERÇÃO MÍNIMA ---")
    conn = None
    try:
        # Vamos usar a conexão padrão (https) para este teste, que é mais simples
        conn = get_db_connection()
        print("[DEBUG] Conexão (HTTPS) estabelecida para o teste.")
        
        # Criamos uma tupla com dados de teste fixos
        dados_fixos = (
            '2025-01-01', 'PRODUTO DE TESTE', 'FORNECEDOR DE TESTE',
            1.0, 'Un', 123.45, 'NOTA_FISCAL_TESTE', 
            st.session_state.get('user_id', 999) # Pega o id do usuário ou usa 999
        )
        
        print(f"[DEBUG] Tentando inserir dados fixos: {dados_fixos}")
        
        # Executamos uma única inserção, sem transação
        conn.execute(
            """INSERT INTO compras (data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal, id_usuario) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            dados_fixos
        )
        
        print("[DEBUG] Comando INSERT executado com sucesso.")
        return True
        
    except Exception as e:
        print(f"\n!!!!!!!!!! [ERRO] ERRO NA INSERÇÃO MÍNIMA !!!!!!!!!!\n{e}")
        st.error(f"Erro na inserção mínima: {e}")
        return False
        
    finally:
        if conn:
            conn.close()
            print("[DEBUG] Conexão de teste fechada.")



def registrar_log(id_usuario, username, acao, detalhes=""):
    """Insere um novo registro na tabela de histórico de atividades no Turso."""
    conn = None
    try:
        conn = get_db_connection()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute(
            """INSERT INTO historico_atividades (id_usuario, username, acao, timestamp, detalhes) VALUES (?, ?, ?, ?, ?)""",
            (id_usuario, username, acao, timestamp, detalhes)
        )
    except Exception as e:
        st.error(f"Erro ao registrar log: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    criar_banco()