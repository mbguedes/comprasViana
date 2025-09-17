import streamlit as st
import pandas as pd
import os
import sqlite3
from datetime import datetime, date
import time

DB_NAME = os.path.join('dados', 'viana.db')

##ARQUIVO_DADOS = os.path.join('dados', 'compras.csv')

if 'compras_stage' not in st.session_state:
    st.session_state.compras_stage = []

##def salvar_dados(df_compras_para_salvar):

def salvar_dados_sql(df_compras_para_salvar):
    """Salva um DataFrame de compras no banco de dados SQLite."""
    try:
        conn = sqlite3.connect(DB_NAME)
        df_compras_para_salvar.to_sql(
            'compras',
            conn,
            if_exists='append',
            index=False
        )
        conn.close()
        st.success("🎉 Todas as compras foram salvas com sucesso no banco de dados!")
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados no banco de dados: {e}")
        return False


        #for _, row in df_compras_para_salvar.iterrows():
        #     cursor.execute("""
        #         INSERT INTO compras (data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal)
        #         VALUES (?, ?, ?, ?, ?, ?, ?)
        #     """, (
        #         row['data_compra'],
        #         row['nome_produto'],
        #         row['fornecedor'],
        #         row['quantidade_comprada'],
        #         row['unidade_medida'],
        #         row['preco_unitario'],
        #         row['numero_nota_fiscal']
        #     ))
        
        #     conn.commit()
        #     st.success("🎉 Todas as compras foram salvas com sucesso no banco de dados!")
        # """Salva um DataFrame de compras no arquivo CSV."""
        # colunas = ['data_compra', 'nome_produto', 'fornecedor', 'quantidade_comprada', 'unidade_medida', 'preco_unitario', 'numero_nota_fiscal']
        # if not os.path.exists(ARQUIVO_DADOS):
        #     os.makedirs('dados', exist_ok=True)
        #     cabecalho = pd.DataFrame(columns=colunas)
        #     cabecalho.to_csv(ARQUIVO_DADOS, index=False, sep=';')
        # df_compras_para_salvar.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False, sep=';')

#FrontEnzo
st.title("📝 Controle de Compras - Restaurante Viana")
st.markdown("---")


with st.form("form_compras", clear_on_submit=True):
    st.subheader("Adicionar Item para Conferência")
    
    col1, col2 = st.columns(2)
    with col1:
        data_compra = st.date_input("Data da compra", value=date.today())
        nome_produto = st.text_input("Nome do produto", placeholder="Ex: Tomate Italiano")
        fornecedor = st.text_input("Fornecedor", placeholder="Ex: Hortifruti do Zé")
        numero_nota_fiscal = st.text_input("Nota Fiscal / Observação", placeholder="Ex: 123456")
    with col2:
        quantidade_comprada = st.number_input("Quantidade", min_value=0.0, format="%.2f")
        unidade_medida = st.text_input("Unidade de Medida", placeholder="Ex: kg, un, L")
        preco_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, format="%.2f")


    submitted = st.form_submit_button("➕ Adicionar à Lista")

if submitted:
    if not nome_produto or preco_unitario == 0:
        st.warning("⚠️ Por favor, preencha pelo menos o Nome do Produto e o Preço Unitário.")
    else:
        st.session_state.compras_stage.append({
            'data_compra': data_compra.strftime('%Y-%m-%d'),
            'nome_produto': nome_produto,
            'fornecedor': fornecedor,
            'quantidade_comprada': quantidade_comprada,
            'unidade_medida': unidade_medida,
            'preco_unitario': preco_unitario,
            'numero_nota_fiscal': numero_nota_fiscal
        })
        st.info("Item adicionado à lista de conferência abaixo.")

st.markdown("---")

# conferencia da lista de compras
if st.session_state.compras_stage:
    st.subheader("Conferência de Lançamentos")
    
    df_stage = pd.DataFrame(st.session_state.compras_stage)
    st.dataframe(df_stage)
    
    col_final1, col_final2 = st.columns(2)
    with col_final1:
        if st.button("💾 Salvar Compras no Banco de Dados", type="primary"):
            if salvar_dados_sql(df_stage):
                placeholder = st.empty()
                placeholder.success("Parabéns! 🎉 Salvo com sucesso!")
                time.sleep(2)
                placeholder.empty()
                st.session_state.compras_stage = []
                st.rerun()

    with col_final2:
        if st.button("Limpar Lista"):
            st.session_state.compras_stage = []
            st.rerun()