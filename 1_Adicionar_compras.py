# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import date
import time

# As funções são importadas aqui e NUNCA redefinidas no resto do arquivo
from autenticacao import check_user, add_user
from database import registrar_log, salvar_dados_sql

# Inicializa o estado da sessão (seções movidas para garantir que rodem antes de tudo)
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.user_id = None

if 'compras_stage' not in st.session_state:
    st.session_state.compras_stage = []

# --- TELA DE LOGIN / CADASTRO ---
if not st.session_state.logged_in:
    st.title("Bem-vindo ao Controle de Compras Viana")
    
    login_tab, signup_tab = st.tabs(["Login", "Criar Conta"])

    with login_tab:
        with st.form("login_form"):
            username = st.text_input("Usuário")
            password = st.text_input("Senha", type="password")
            access_key_login = st.text_input("Palavra-chave de Acesso", type="password", placeholder="Validação de funcionário", key="login_keyword")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                # (Lógica de login continua a mesma)
                pass # Cole sua lógica de login aqui

    with signup_tab:
        with st.form("signup_form"):
            # (Lógica de criar conta continua a mesma)
            pass # Cole sua lógica de signup aqui
else:
    # --- APLICAÇÃO PRINCIPAL (SÓ APARECE DEPOIS DO LOGIN) ---
    
    st.sidebar.success(f"Logado como: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # --- A FUNÇÃO DUPLICADA FOI REMOVIDA DAQUI ---

    # --- INÍCIO DA INTERFACE PRINCIPAL ---
    st.title("📝 Restaurante Viana Praia")
    st.subheader("Sistema de Controle de Compras")
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
            unidade_medida = st.selectbox(
                'Unidade de Medida',
                options=['Un','L','Kg','Cxa','Pct']
            )
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
                'numero_nota_fiscal': numero_nota_fiscal,
                'id_usuario': st.session_state.user_id
            })
            st.info("Item adicionado à lista de conferência abaixo.")

    st.markdown("---")
        
    if st.session_state.compras_stage:
        st.subheader("Conferência de Lançamentos")
        
        df_stage = pd.DataFrame(st.session_state.compras_stage)
        st.dataframe(df_stage)
        
        col_final1, col_final2 = st.columns(2)
        with col_final1:
            if st.button("💾 Salvar Compras no Banco de Dados", type="primary"):
                if salvar_dados_sql(df_stage): # Agora esta chamada usa a função CORRETA do database.py
                    detalhes_log = f"O usuário salvou {len(df_stage)} novos itens de compra."
                    registrar_log(
                        id_usuario=st.session_state.user_id,
                        username=st.session_state.username,
                        acao="REGISTRO DE COMPRAS",
                        detalhes=detalhes_log
                    )
                    
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