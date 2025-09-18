import sqlite3
import pandas as pd
import random
from faker import Faker
from datetime import datetime

DB_NAME = 'dados/viana.db'
NUM_REGISTROS = 80

# Inicializa o Faker para gerar dados em português do Brasil
fake = Faker('pt_BR')

PRODUTOS = [
    ('Tomate Italiano', 8.50, 'Kg'),
    ('Cebola Pera', 5.00, 'Kg'),
    ('Batata Asterix', 6.00, 'Kg'),
    ('Filé Mignon', 85.00, 'Kg'),
    ('Peito de Frango', 18.00, 'Kg'),
    ('Arroz Agulhinha T1', 25.00, 'Un'),
    ('Feijão Carioca', 9.00, 'Un'),
    ('Óleo de Soja', 8.00, 'Un'),
    ('Azeite Extra Virgem', 35.00, 'Un'),
    ('Pão Francês', 15.00, 'Kg'),
    ('Queijo Mussarela', 45.00, 'Kg'),
    ('Vinho Tinto Seco', 40.00, 'Un'),
    ('Refrigerante 2L', 10.00, 'Un'),
    ('Água Mineral 500ml 12un', 30.00, 'Cxa')
]

#usando o faker pra gerar nomes fictícios de fornecedores
FORNECEDORES = [fake.company() for _ in range(5)]

def popular_banco():
    """Gera dados falsos e os insere no banco de dados SQLite."""
    
    lista_de_compras = []
    print(f"Gerando {NUM_REGISTROS} registros de compras falsas...")

    for _ in range(NUM_REGISTROS):
        produto_nome, preco_base, unidade = random.choice(PRODUTOS)
        fornecedor = random.choice(FORNECEDORES)
        
        # Gera dados aleatórios para cada campo
        data_compra = fake.date_time_between(start_date='-2y', end_date='now').strftime('%Y-%m-%d')
        
        if unidade == 'Kg':
            quantidade = round(random.uniform(5.0, 50.0), 2)
        else:
            quantidade = random.randint(1, 10)
        ##variacao de preço aleatória de até 15%
        preco_unitario = round(preco_base * random.uniform(0.85, 1.15), 2)
        
        numero_nota_fiscal = str(fake.random_int(min=111, max=9999))
        
        lista_de_compras.append({
            'data_compra': data_compra,
            'nome_produto': produto_nome,
            'fornecedor': fornecedor,
            'quantidade_comprada': quantidade,
            'unidade_medida': unidade,
            'preco_unitario': preco_unitario,
            'numero_nota_fiscal': numero_nota_fiscal
        })

    df_compras = pd.DataFrame(lista_de_compras)
    
    try:
        conn = sqlite3.connect(DB_NAME)
        df_compras.to_sql('compras', conn, if_exists='append', index=False)
        conn.close()
        print(f"\n✅ Sucesso! {NUM_REGISTROS} registros foram adicionados à tabela 'compras'.")
    except Exception as e:
        print(f"\nErro ao salvar no banco de dados: {e}")

if __name__ == '__main__':
    popular_banco()