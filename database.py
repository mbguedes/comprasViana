# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados PostgreSQL."""
    conn_str = ""
    try:
        conn_str = st.secrets["DATABASE_URL"]
    except Exception:
        load_dotenv()
        conn_str = os.getenv("DATABASE_URL")
    
    if not conn_str:
        raise ValueError("URL do banco de dados não encontrada.")
        
    return psycopg2.connect(conn_str, client_encoding='UTF8')

def criar_banco():
    """Verifica e cria as tabelas no banco de dados PostgreSQL."""
    commands = [
        """CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL);""",
        """CREATE TABLE IF NOT EXISTS compras (id SERIAL PRIMARY KEY, data_compra DATE NOT NULL, nome_produto TEXT NOT NULL, fornecedor TEXT, quantidade_comprada REAL NOT NULL, unidade_medida TEXT NOT NULL, preco_unitario REAL NOT NULL, numero_nota_fiscal TEXT, id_usuario INTEGER, FOREIGN KEY(id_usuario) REFERENCES usuarios(id));""",
        """CREATE TABLE IF NOT EXISTS historico_atividades (id SERIAL PRIMARY KEY, id_usuario INTEGER, username TEXT NOT NULL, acao TEXT NOT NULL, timestamp TIMESTAMP NOT NULL, detalhes TEXT, FOREIGN KEY(id_usuario) REFERENCES usuarios(id));"""
    ]
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()
        print("✅ Tabelas verificadas/criadas no PostgreSQL com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas no PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()

def ler_dados_sql():
    """Lê todos os dados da tabela 'compras' do Postgres."""
    conn = None
    try:
        conn = get_db_connection()
        query = "SELECT c.*, u.username as registrado_por FROM compras c LEFT JOIN usuarios u ON c.id_usuario = u.id ORDER BY c.data_compra DESC"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Erro ao ler dados do banco: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

def salvar_dados_sql(df_compras_para_salvar):
    """Salva um DataFrame de compras no banco de dados PostgreSQL."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for _, row in df_compras_para_salvar.iterrows():
            cursor.execute(
                "INSERT INTO compras (data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal, id_usuario) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (row['data_compra'], row['nome_produto'], row['fornecedor'], row['quantidade_comprada'], row['unidade_medida'], row['preco_unitario'], row['numero_nota_fiscal'], row['id_usuario'])
            )
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        st.error(f"Erro detalhado ao salvar dados: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def registrar_log(id_usuario, username, acao, detalhes=""):
    """Insere um novo registro na tabela de histórico de atividades no PostgreSQL."""
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        timestamp = datetime.now()
        sql = "INSERT INTO historico_atividades (id_usuario, username, acao, timestamp, detalhes) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_usuario, username, acao, timestamp, detalhes))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        st.error(f"Erro ao registrar log: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    print("Executando script de setup do banco de dados...")
    criar_banco()