import pandas as pd
import os
from datetime import datetime

ARQUIVO_DADOS = os.path.join('dados', 'compras.csv')

def adicionar_compra():
    """
    Coleta os dados de uma nova compra do usuário e a adiciona ao arquivo CSV.
    """
    print('--- Adicionando Nova Compra ---')
    
    data_hoje = datetime.now().strftime('%Y-%m-%d')
    data_digitada = input(f"Data da compra (AAAA-MM-DD) [Pressione Enter para usar hoje ({data_hoje})]: ")
    
    if not data_digitada:
        data_compra = data_hoje
    else:
        data_compra = data_digitada


    nome_produto = input('Nome do produto: ')
    fornecedor = input('Fornecedor: ')
    quantidade_comprada = float(input('Quantidade comprada (ex: 2.5): '))
    unidade_medida = input('Unidade de medida (ex: kg, un, lt): ')
    preco_unitario = float(input('Preço unitário (ex: 8.20): '))
    numero_nota_fiscal = input('Número da nota fiscal ou alguma obs: ')

    custo_total = preco_unitario * quantidade_comprada
    print(f'\nCusto total do item: R$ {custo_total:.2f}')

    novo_registro = {
        'data_compra': [data_compra],
        'nome_produto': [nome_produto],
        'fornecedor': [fornecedor],
        'quantidade_comprada': [quantidade_comprada],
        'unidade_medida': [unidade_medida],
        'preco_unitario': [preco_unitario],
        'numero_nota_fiscal': [numero_nota_fiscal]
    }

    df_novo = pd.DataFrame(novo_registro)

    df_novo.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False, sep=';')

    print('\n✅ Compra adicionada com sucesso!')