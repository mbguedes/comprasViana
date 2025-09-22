import streamlit as st
import pandas as pd
from database import salvar_dados_sql # Importamos APENAS a função de salvar
import time

# Código de guarda para garantir que o usuário está logado
if not st.session_state.get("logged_in", False):
    st.error("❌ Acesso negado! Por favor, faça o login para executar os testes.")
    st.stop()

st.title("🧪 Página de Teste de Gravação no Banco")
st.markdown("---")
st.warning("Esta página é para depuração. Ela tenta inserir dados fixos no banco de dados.")

# 1. Criamos um DataFrame de teste com dados fixos
# Certifique-se de que os nomes das colunas são EXATAMENTE os mesmos da sua tabela
dados_teste = {
    'data_compra': ['2025-09-22'],
    'nome_produto': ['PRODUTO DE TESTE'],
    'fornecedor': ['FORNECEDOR TESTE'],
    'quantidade_comprada': [10.0],
    'unidade_medida': ['Un'],
    'preco_unitario': [99.99],
    'numero_nota_fiscal': ['TESTE123'],
    'id_usuario': [st.session_state.get('user_id', None)] # Pega o ID do usuário logado
}
df_teste = pd.DataFrame(dados_teste)

st.subheader("Dados que serão inseridos:")
st.dataframe(df_teste)

# 2. Criamos um botão para disparar o teste
if st.button("Executar Teste de Gravação Direta", type="primary"):
    st.info("Iniciando o teste de gravação...")

    # 3. Chamamos a função de salvar com os dados de teste
    sucesso = salvar_dados_sql(df_teste)

    # 4. Exibimos um resultado claro na tela
    if sucesso:
        st.success("✅ TESTE BEM-SUCEDIDO! A função 'salvar_dados_sql' retornou 'True'.")
        st.write("Verifique o banco de dados Turso para confirmar se a linha 'PRODUTO DE TESTE' foi adicionada.")
        st.balloons()
    else:
        st.error("❌ TESTE FALHOU! A função 'salvar_dados_sql' retornou 'False'. Verifique os logs no 'Manage app' para ver o erro detalhado.")