-- Este arquivo define a estrutura completa do nosso banco de dados.

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS compras (
    id SERIAL PRIMARY KEY,
    data_compra DATE NOT NULL,
    nome_produto TEXT NOT NULL,
    fornecedor TEXT,
    quantidade_comprada REAL NOT NULL,
    unidade_medida TEXT NOT NULL,
    preco_unitario REAL NOT NULL,
    numero_nota_fiscal TEXT,
    id_usuario INTEGER,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);

CREATE TABLE IF NOT EXISTS historico_atividades (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER,
    username TEXT NOT NULL,
    acao TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    detalhes TEXT,
    FOREIGN KEY(id_usuario) REFERENCES usuarios(id)
);