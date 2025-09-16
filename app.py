import streamlit as st
import pandas as pd
import os
from datetime import datetime, date


ARQUIVO_DADOS = os.path.join('dados', 'compras.csv')

def salvar_dados(data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal):
    """Salva um novo registro de compra no arquivo CSV."""
    

    colunas = ['data_compra', 'nome_produto', 'fornecedor', 'quantidade_comprada', 'unidade_medida', 'preco_unitario', 'numero_nota_fiscal']


    if not os.path.exists(ARQUIVO_DADOS):
        os.makedirs('dados', exist_ok=True)
        cabecalho = pd.DataFrame(columns=colunas)
        cabecalho.to_csv(ARQUIVO_DADOS, index=False, sep=';')


    novo_registro = pd.DataFrame([[data_compra, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal]], columns=colunas)
    

    novo_registro.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False, sep=';')


# FRONTENZO ---

st.title("📝 Controle de Compras - Restaurante Viana")

st.markdown("--------")

with st.form("form_compras"):
    st.subheader("Registrar Nova Compra")

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


    submitted = st.form_submit_button("✔️ Registrar Compra")


if submitted:

    if not nome_produto or preco_unitario == 0:
        st.error("⚠️ Por favor, preencha pelo menos o Nome do Produto e o Preço Unitário.")
    else:

        data_compra_str = data_compra.strftime('%Y-%m-%d')
        

        salvar_dados(data_compra_str, nome_produto, fornecedor, quantidade_comprada, unidade_medida, preco_unitario, numero_nota_fiscal)
        

        st.success("🎉 Compra registrada com sucesso!")
        st.balloons()