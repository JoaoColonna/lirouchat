# Lirouchat

Projeto desenvolvido para o Trabalho de Conclusão de Curso (TCC).

## Descrição

[Lirouchat](https://github.com/JoaoColonna/lirouchat) é um chatbot em API RESTful usando Python e Django-Ninja.
- Utiliza como IA o Gemini, onde você pode utilizar sua chave em uma variável de ambiente.
```.env
  gemini_api_key=sua_api_key
```

- Para ver o Swagger e os endpoints da API (rodando localmente), acesse:
```url
  http://127.0.0.1:8000/chatbot/api/docs#/default
```

## Funcionalidades

A API oferece as seguintes funcionalidades:

**Autenticação de Usuário:**

- **Login:** Permite que um usuário faça login no sistema.
- **Logout:** Permite que um usuário faça logout do sistema.
- **Troca de Senha:** Permite que um usuário altere sua senha.
- **Teste de Autenticação:** Endpoint protegido para testar a autenticação do usuário.

**Gerenciamento de Usuários:**

- **Criação de Usuário:** Permite a criação de um novo usuário.
- **Atualização de Usuário:** Permite a atualização das informações de um usuário existente.
- **Exclusão de Usuário:** Permite a exclusão de um usuário.
- **Listagem de Usuários:** Permite listar todos os usuários.

**Interação com o Chatbot:**

- **Enviar Mensagem:** Permite enviar uma mensagem para o chatbot e receber uma resposta.
- **Obter Conversa:** Permite obter todas as mensagens de uma conversa específica.
- **Obter Título da Conversa:** Permite obter o título de uma conversa específica.


## Instalação e inicialização

Antes de tudo, você deve ter o Python 3.12 instalado em sua maquina, junto com o pip (gerenciador de pacotes do python)
Siga os passos abaixo para instalar e iniciar o projeto:

1. Clone o repositório
    ```sh
    git clone https://github.com/JoaoColonna/lirouchat.git
    ```
2. Entre no diretório do projeto
    ```sh
    cd lirouchat
    ```
3. Instale as dependências
    ```sh
    pip install -r requirements.txt
    ```
4. Execute as migrações
    ```sh
    python manage.py migrate
    ```
5. Inicie o servidor
    ```sh
    python manage.py runserver
    ```
