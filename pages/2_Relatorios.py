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

# Carrega a totalidade dos dados do banco
df_completo = ler_dados_sql()

# --- INÍCIO DO BLOCO DE DEBUGGING ---
st.subheader("🕵️‍♂️ Informações de Depuração (Temporário)")
st.write("Abaixo estão os dados brutos recebidos do banco, ANTES de qualquer filtro:")
st.write(f"**Número total de linhas na tabela 'compras':** `{len(df_completo)}`")
if not df_completo.empty:
    st.write("**Colunas recebidas:**", df_completo.columns.tolist())
st.dataframe(df_completo)
st.markdown("---")
# --- FIM DO BLOCO DE DEBUGGING ---

# --- BOTÕES DE FILTRO PRINCIPAL ---
if 'show_only_mine' not in st.session_state:
    st.session_state.show_only_mine = False

col_botoes1, col_botoes2, _ = st.columns([1, 1, 4])
with col_botoes1:
    if st.button("Meus Lançamentos", use_container_width=True, type="primary"):
        st.session_state.show_only_mine = True
        st.rerun()

with col_botoes2:
    if st.button("Mostrar Todos", use_container_width=True):
        st.session_state.show_only_mine = False
        st.rerun()

# --- LÓGICA PARA APLICAR O FILTRO ---
if st.session_state.show_only_mine:
    df_display = df_completo[df_completo['id_usuario'] == st.session_state.user_id]
    st.info(f"Exibindo apenas os lançamentos de **{st.session_state.username}**.")
else:
    df_display = df_completo
    st.info("Exibindo todos os lançamentos.")

# O resto da sua página continua igual, usando df_display
if df_display.empty:
    st.warning("⚠️ Nenhum registro encontrado para a seleção atual.")
else:
    # ... (seu código de subheaders, filtros, métricas e gráficos continua aqui)
    pass # Remova este 'pass' e cole o resto do seu código aqui