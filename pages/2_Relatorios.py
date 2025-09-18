import streamlit as st
import pandas as pd
from database import ler_dados_sql

# --- CÓDIGO DE GUARDA / VERIFICAÇÃO DE LOGIN ---
if not st.session_state.get("logged_in", False):
    st.error("❌ Acesso negado! Por favor, faça o login na página principal para acessar os relatórios.")
    st.stop()

# --- INTERFACE CONSISTENTE (Logout na Sidebar) ---
st.sidebar.success(f"Logado como: {st.session_state.username}")
if st.sidebar.button("Logout", key="logout_relatorios"):
    # Limpa todas as chaves da sessão para garantir um logout limpo
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- INÍCIO DA PÁGINA DE RELATÓRIOS ---
st.set_page_config(layout="wide")
st.title("📊 Relatórios de Compras")
st.markdown("---")

# --- 1. INICIALIZAÇÃO DO ESTADO DO FILTRO ---
if 'show_only_mine' not in st.session_state:
    st.session_state.show_only_mine = False

# --- 2. BOTÕES DE FILTRO PRINCIPAL ---
col_botoes1, col_botoes2, _ = st.columns([1, 1, 4]) # Adiciona colunas para alinhar
with col_botoes1:
    if st.button("Meus Lançamentos", use_container_width=True, type="primary"):
        st.session_state.show_only_mine = True
        st.rerun()

with col_botoes2:
    if st.button("Mostrar Todos", use_container_width=True):
        st.session_state.show_only_mine = False
        st.rerun()

# Carrega a totalidade dos dados do banco
df_completo = ler_dados_sql()

# --- 3. LÓGICA PARA APLICAR O FILTRO ---
# Cria um DataFrame de exibição com base no estado do filtro
if st.session_state.show_only_mine:
    # Filtra o DataFrame para mostrar apenas os registros do usuário logado
    df_display = df_completo[df_completo['id_usuario'] == st.session_state.user_id]
    st.info(f"Exibindo apenas os lançamentos de **{st.session_state.username}**.")
else:
    df_display = df_completo
    st.info("Exibindo todos os lançamentos.")


# --- 4. O RESTO DA PÁGINA AGORA USA 'df_display' ---
if df_display.empty:
    st.warning("⚠️ Nenhum registro encontrado para a seleção atual.")
else:
    st.subheader("Visão Geral das Compras")
    st.dataframe(df_display)

    st.markdown("---")

    st.subheader("Análise Detalhada por Produto")
    # O filtro de produto agora opera sobre os dados já pré-filtrados (todos ou meus)
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

    # Adicionado um 'if' para evitar erro de divisão por zero se não houver preço
    preco_medio = df_filtrado_final['preco_unitario'].mean() if not df_filtrado_final.empty else 0
    col2.metric("Preço Médio Unitário", f"R$ {preco_medio:,.2f}")
    
    num_registros = len(df_filtrado_final)
    col3.metric("Nº de Compras Registradas", num_registros)

    if produto_selecionado != "Todos" and not df_filtrado_final.empty:
        st.markdown(f"#### Evolução do Preço Unitário de '{produto_selecionado}'")
        df_grafico = df_filtrado_final.set_index('data_compra')
        st.line_chart(df_grafico['preco_unitario'])