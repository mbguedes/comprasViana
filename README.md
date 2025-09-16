# 📝 Controle de Compras - Restaurante Viana

Uma aplicação web simples, desenvolvida em Python, para registrar e controlar os preços de compra de produtos para o Restaurante Viana. O objetivo é substituir o controle manual em planilhas e fornecer um histórico rápido de custos.

## ✨ Funcionalidades Atuais

-   **Registro de Novas Compras:** Formulário web amigável para inserir detalhes de cada compra, como produto, fornecedor, quantidade, preço, etc.
-   **Armazenamento de Dados:** As informações são salvas de forma estruturada em um arquivo CSV.
-   **Interface Intuitiva:** Desenvolvido com Streamlit para garantir uma experiência de uso simples e direta, sem a necessidade de usar o terminal.

## 🛠️ Tecnologias Utilizadas

-   **Python 3**
-   **Streamlit:** Para a criação da interface web (front-end).
-   **Pandas:** Para a manipulação e armazenamento dos dados no arquivo CSV.

## 🚀 Como Instalar e Executar o Projeto

Siga os passos abaixo para rodar a aplicação em sua máquina local.

### Pré-requisitos

-   [Python 3.8+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/downloads/)

### Passo a Passo

1.  **Clone o repositório:**
    Abra seu terminal e execute o comando abaixo para baixar os arquivos do projeto.
    ```bash
    git clone [https://github.com/mbguedes/comprasViana.git](https://github.com/mbguedes/comprasViana.git)
    ```

2.  **Navegue até a pasta do projeto:**
    ```bash
    cd comprasViana
    ```

3.  **Crie e ative um ambiente virtual:**
    Isso isola as dependências do projeto.
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar o ambiente (Windows)
    .\venv\Scripts\activate

    # Ativar o ambiente (macOS/Linux)
    source venv/bin/activate
    ```

4.  **Instale as dependências:**
    Este comando lerá o arquivo `requirements.txt` e instalará todas as bibliotecas necessárias de uma vez.
    ```bash
    pip install -r requirements.txt
    ```

### Como Executar a Aplicação

Com o ambiente virtual ativo e as dependências instaladas, execute o seguinte comando no terminal:


streamlit run app.py


ESTRUTURA --

/comprasViana/
|-- /dados/              # Pasta onde o arquivo de compras será salvo
|-- .gitignore           # Arquivos e pastas a serem ignorados pelo Git
|-- app.py               # Código principal da aplicação Streamlit (front-end)
|-- requirements.txt     # Lista de dependências Python para instalação
|-- README.md            # Este arquivo


