import streamlit as st
import pandas as pd
from datetime import datetime
import libsql_client
import os
from dotenv import load_dotenv # Importa a nova biblioteca

# --- FUNÇÃO DE CONEXÃO HÍBRIDA ---
def get_db_connection(for_transaction: bool = False):
    """Cria uma conexão com o Turso, lendo segredos do Streamlit Cloud ou de um arquivo .env local."""
    
    # Tenta carregar os segredos do Streamlit Cloud
    try:
        url = st.secrets["TURSO_DB_URL"]
        auth_token = st.secrets["TURSO_AUTH_TOKEN"]
    # Se falhar (estamos em um terminal local), carrega do .env
    except Exception:
        load_dotenv()
        url = os.getenv("TURSO_DB_URL")
        auth_token = os.getenv("TURSO_AUTH_TOKEN")
        
    if not url or not auth_token:
        raise ValueError("Credenciais do banco de dados não encontradas. Verifique seus arquivos secrets.toml ou .env")

    # Lógica de protocolo (https vs wss)
    if for_transaction:
        if url.startswith("libsql://"):
            url = url.replace("libsql://", "wss://")
    else:
        if url.startswith("libsql://"):
            url = url.replace("libsql://", "https://")
            
    return libsql_client.create_client_sync(url=url, auth_token=auth_token)

# --- FUNÇÕES DE MANIPULAÇÃO DO BANCO ---
# Nenhuma outra função precisa ser alterada. O código abaixo é o que você já tem.

def criar_banco():
    """Verifica e cria as tabelas no banco de dados Turso se não existirem."""
    conn = None
    try:
        # Vamos usar a conexão padrão (https), que é mais estável.
        conn = get_db_connection()
        print("Conectado ao banco de dados (via https).")
        
        # Executamos um comando CREATE TABLE de cada vez.
        print("Criando/verificando a tabela 'usuarios'...")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            );
        """)
        
        print("Criando/verificando a tabela 'compras'...")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS compras (
                id INTEGER PRIMARY KEY AUTOINCREMENT, data_compra TEXT NOT NULL, nome_produto TEXT NOT NULL,
                fornecedor TEXT, quantidade_comprada REAL NOT NULL, unidade_medida TEXT NOT NULL,
                preco_unitario REAL NOT NULL, numero_nota_fiscal TEXT, id_usuario INTEGER,
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
            );
        """)

        print("Criando/verificando a tabela 'historico_atividades'...")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS historico_atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT, id_usuario INTEGER, username TEXT NOT NULL,
                acao TEXT NOT NULL, timestamp TEXT NOT NULL, detalhes TEXT,
                FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
            );
        """)

        print("✅ Tabelas verificadas/criadas no Turso com sucesso.")
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas no Turso: {e}")
    finally:
        if conn:
            conn.close()

def ler_dados_sql():
    conn = None
    try:
        conn = get_db_connection()
        query = "SELECT c.*, u.username as registrado_por FROM compras c LEFT JOIN usuarios u ON c.id_usuario = u.id ORDER BY c.data_compra DESC"
        rs = conn.execute(query)
        df = pd.DataFrame(rs.rows, columns=rs.columns)
        if not df.empty and 'data_compra' in df.columns:
            df['data_compra'] = pd.to_datetime(df['data_compra'])
        return df
    except Exception as e:
        st.error(f"Erro ao ler dados do banco: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def salvar_dados_sql(df_compras_para_salvar):
    conn = None
    try:
        conn = get_db_connection(for_transaction=True)
        with conn.transaction() as tx:
            for _, row in df_compras_para_salvar.iterrows():
                tx.execute(
                    """INSERT INTO compras (data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal, id_usuario) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (row['data_compra'], row['nome_produto'], row['fornecedor'], row['quantidade_comprada'], row['unidade_medida'], row['preco_unitario'], row['numero_nota_fiscal'], row['id_usuario'])
                )
        return True
    except Exception as e:
        st.error(f"Erro detalhado ao salvar dados: {e}")
        return False
    finally:
        if conn:
            conn.close()

def registrar_log(id_usuario, username, acao, detalhes=""):
    # --- FINGERPRINT ---
    print(f"[FINGERPRINT] Executando registrar_log da versão: {DATABASE_PY_VERSION}")
    conn = None
    try:
        conn = get_db_connection(for_transaction=True)
        with conn.transaction() as tx:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tx.execute(
                """INSERT INTO historico_atividades (id_usuario, username, acao, timestamp, detalhes) VALUES (?, ?, ?, ?, ?)""",
                (id_usuario, username, acao, timestamp, detalhes)
            )
    except Exception as e:
        st.error(f"Erro ao registrar log: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print('Executando script de setup do banco de dados...')
    criar_banco()