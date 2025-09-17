import streamlit as st
import pandas as pd
from database import ler_dados_sql

st.set_page_config(layout="wide")

st.title("📊 Relatórios de Compras")
st.markdown("---")

df = ler_dados_sql()

if df.empty:
    st.warning("⚠️ Ainda não há compras registradas no banco de dados.")
else:

    st.subheader("Visão Geral de Todas as Compras")
    st.dataframe(df)

    st.markdown("---")


    st.subheader("Análise Detalhada por Produto")


    produtos = ["Todos"] + sorted(df['nome_produto'].unique())
    produto_selecionado = st.selectbox("Selecione um produto para analisar:", options=produtos)
    

    if produto_selecionado == "Todos":
        df_filtrado = df
    else:
        df_filtrado = df[df['nome_produto'] == produto_selecionado]


    st.markdown("#### Métricas Principais")
    col1, col2, col3 = st.columns(3)

    custo_total = (df_filtrado['quantidade_comprada'] * df_filtrado['preco_unitario']).sum()
    col1.metric("Custo Total", f"R$ {custo_total:,.2f}")

    preco_medio = df_filtrado['preco_unitario'].mean()
    col2.metric("Preço Médio Unitário", f"R$ {preco_medio:,.2f}")

    num_registros = len(df_filtrado)
    col3.metric("Nº de Compras Registradas", num_registros)

    if produto_selecionado != "Todos" and not df_filtrado.empty:
        st.markdown(f"#### Evolução do Preço Unitário de '{produto_selecionado}'")

        df_grafico = df_filtrado.set_index('data_compra')
        
        st.line_chart(df_grafico['preco_unitario'])