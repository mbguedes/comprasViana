import pandas as pd
import os
from datetime import datetime

ARQUIVO_DADOS = os.path.join('dados', 'compras.csv')

def adicionar_compra():
    print('Adicionando nova compra...')

    data_compra = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    nome_produto = input('Nome do produto: ')
    fornecedor = input('Fornecedor: ')
    preco_unitario = float(input('Preço unitário (use . para centavos, ex: 8.20): '))
    unidade_medida = input('Unidade de medida (ex: kg, un, lt): ')
    quantidade_comprada = float(input('Quantidade comprada (use . para centavos, ex: 2.5): '))
    numero_nota_fiscal = input('Número da nota fiscal ou alguma obs: ')

    custo_total = preco_unitario * quantidade_comprada

    novo_registro = {
        'Data da Compra': [data_compra],
        'Nome do Produto': [nome_produto],
        'Fornecedor': [fornecedor],
        'Quantidade Comprada': [quantidade_comprada],
        'Unidade de Medida': [unidade_medida],
        'Preço Unitário': [preco_unitario],
        'Número da Nota Fiscal': [numero_nota_fiscal]
    }

    df_novo = pd.DataFrame(novo_registro)

    df_novo.to_csv(ARQUIVO_DADOS, mode='a', header=False, index=False, sep=';')

    print('Compra adicionada com sucesso!')
    # print(f'Compra de {quantidade_comprada} {unidade_medida} de {nome_produto} por R$ {custo_total:.2f} adicionada com sucesso!')

if __name__ == '__main__':
    colunas = ['data_compra', 'nome_produto', 'fornecedor', 'quantidade_comprada', 'unidade_medida', 'preco_unitario', 'numero_nota_fiscal']
    
    if not os.path.isfile(ARQUIVO_DADOS):
        print('Arquivo não encontrado. Criando um novo...')
        os.makedirs('dados', exist_ok=True)

        cabecalho = pd.DataFrame(columns=colunas)
        cabecalho.to_csv(ARQUIVO_DADOS, index=False, sep=';')

    adicionar_compra()
