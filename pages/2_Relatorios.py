# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from database import ler_dados_sql

# st.set_page_config() deve ser o primeiro comando Streamlit
st.set_page_config(layout="wide") 

# --- CÓDIGO DE GUARDA / VERIFICAÇÃO DE LOGIN ---
if not st.session_state.get("logged_in", False):
    st.error("❌ Acesso negado! Por favor, faça o login na página principal.")
    st.stop()

# --- INTERFACE CONSISTENTE (Logout na Sidebar) ---
st.sidebar.success(f"Logado como: {st.session_state.username}")
if st.sidebar.button("Logout", key="logout_relatorios"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- INÍCIO DA PÁGINA DE RELATÓRIOS ---
st.title("📊 Relatórios de Compras")
st.markdown("---")

# --- BOTÕES DE FILTRO PRINCIPAL ---
if 'show_only_mine' not in st.session_state:
    st.session_state.show_only_mine = False

col_botoes1, col_botoes2, _ = st.columns([1.5, 2, 4]) # Ajuste no layout dos botões
with col_botoes1:
    if st.button("Meus Lançamentos", use_container_width=True, type="primary"):
        st.session_state.show_only_mine = True
        st.rerun()

with col_botoes2:
    if st.button("Mostrar Todos os Lançamentos", use_container_width=True):
        st.session_state.show_only_mine = False
        st.rerun()

# Carrega a totalidade dos dados do banco
df_completo = ler_dados_sql()

# --- LÓGICA PARA APLICAR O FILTRO (COM CORREÇÃO DE TIPO) ---
if st.session_state.show_only_mine:
    # Garante que a coluna 'id_usuario' seja numérica, lida com valores ausentes e a converte para inteiro.
    df_completo['id_usuario'] = pd.to_numeric(df_completo['id_usuario'], errors='coerce').fillna(0).astype(int)
    
    # Garante que o user_id da sessão também seja um inteiro para a comparação.
    user_id_int = int(st.session_state.user_id)
    
    # Aplica o filtro com os tipos de dados consistentes.
    df_display = df_completo[df_completo['id_usuario'] == user_id_int]
    
    st.info(f"Exibindo apenas os lançamentos de **{st.session_state.username}**.")
else:
    df_display = df_completo
    st.info("Exibindo todos os lançamentos.")


# --- O RESTO DA PÁGINA USA 'df_display' ---
if df_display.empty:
    st.warning("⚠️ Nenhum registro encontrado para a seleção atual.")
else:
    st.subheader("Visão Geral das Compras")
    st.dataframe(df_display)

    st.markdown("---")

    st.subheader("Análise Detalhada por Produto")
    produtos = ["Todos"] + sorted(df_display['nome_produto'].unique())
    produto_selecionado = st.selectbox("Selecione um produto para analisar:", options=produtos)
    
    if produto_selecionado == "Todos":
        df_filtrado_final = df_display
    else:
        df_filtrado_final = df_display[df_display['nome_produto'] == produto_selecionado]

    st.markdown("#### Métricas Principais")
    col1, col2, col3 = st.columns(3)
    
    custo_total = (df_filtrado_final['quantidade_comprada'] * df_filtrado_final['preco_unitario']).sum()
    col1.metric("Custo Total", f"R$ {custo_total:,.2f}")

    preco_medio = df_filtrado_final['preco_unitario'].mean() if not df_filtrado_final.empty else 0
    col2.metric("Preço Médio Unitário", f"R$ {preco_medio:,.2f}")
    
    num_registros = len(df_filtrado_final)
    col3.metric("Nº de Compras Registradas", num_registros)

    if produto_selecionado != "Todos" and not df_filtrado_final.empty:
        st.markdown(f"#### Evolução do Preço Unitário de '{produto_selecionado}'")
        df_grafico = df_filtrado_final.set_index('data_compra')
        st.line_chart(df_grafico['preco_unitario'])