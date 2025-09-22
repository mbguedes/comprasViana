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

def salvar_dados_sql(df_compras_para_salvar):
    """Salva um DataFrame de compras no banco de dados Turso com debug super verboso."""
    
    # Imprime no log do terminal exatamente o que a função recebeu
    print("\n--- [DEBUG] INICIANDO PROCESSO DE SALVAMENTO ---")
    print(f"[DEBUG] DataFrame recebido com {len(df_compras_para_salvar)} linhas.")
    
    # Verifica se o DataFrame não está vazio e imprime colunas e tipos de dados
    if not df_compras_para_salvar.empty:
        print("[DEBUG] Colunas do DataFrame:", df_compras_para_salvar.columns.tolist())
        print("[DEBUG] Tipos de dados (dtypes):\n", df_compras_para_salvar.dtypes)
    
    conn = None
    try:
        conn = get_db_connection()
        print("[DEBUG] Conexão com o banco de dados Turso estabelecida.")
        
        # Usa uma transação para garantir a integridade dos dados
        with conn.transaction() as tx:
            print("[DEBUG] Transação iniciada.")
            for i, row in df_compras_para_salvar.iterrows():
                # Prepara a tupla de valores para inserção
                valores_para_inserir = (
                    row['data_compra'], row['nome_produto'], row['fornecedor'],
                    row['quantidade_comprada'], row['unidade_medida'], row['preco_unitario'],
                    row['numero_nota_fiscal'], row['id_usuario']
                )
                print(f"[DEBUG] Inserindo linha {i+1}: {valores_para_inserir}")
                tx.execute(
                    """INSERT INTO compras (data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal, id_usuario) 
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    valores_para_inserir
                )
        
        # Se o bloco 'with' terminar sem erros, o commit é automático
        print("[DEBUG] Transação CONCLUÍDA com sucesso.")
        return True
        
    except Exception as e:
        # Imprime o erro detalhado no log do terminal e também na tela do app
        print("\n\n!!!!!!!!!! [ERRO] ERRO CAPTURADO DURANTE O SALVAMENTO !!!!!!!!!!\n")
        print(f"[ERRO] TIPO DE EXCEÇÃO: {type(e)}")
        print(f"[ERRO] MENSAGEM: {e}")
        print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
        st.error(f"Erro detalhado ao salvar dados: {e}")
        return False
        
    finally:
        if conn:
            conn.close()
            print("[DEBUG] Conexão com o banco fechada.")

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