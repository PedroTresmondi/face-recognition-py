# ⚠️WIP⚠️

## Face Recognition Authentication System

### Descrição do Projeto

Este projeto é um sistema de autenticação facial que utiliza a webcam para detectar e reconhecer rostos, autenticando usuários com base em suas características faciais. O backend é desenvolvido em Python e está em deploy no Fly.io, permitindo que a autenticação funcione sem a necessidade de rodar o backend localmente. O frontend é desenvolvido com Vite.

### Funcionalidades

- Captura de vídeo em tempo real através da webcam.
- Detecção e reconhecimento de rostos no quadro de vídeo.
- Codificação e comparação de rostos utilizando a biblioteca `face_recognition`.
- Interface de usuário interativa desenvolvida com Vite.
- Integração com Firebase para armazenamento e autenticação de dados.

### Estrutura de Arquivos

<pre>
FACE-RECOGNITION-AUTHENTICATION/
├── backend/
│   ├── Images/
│   ├── Resources/
│   ├── __pycache__/
│   ├── .env
│   ├── AddDataToDatabase.py
│   ├── app.py
│   ├── backupCode.py
│   ├── encodeFile.p
│   ├── EncodeGenerator.py
│   ├── firebase_config.py
│   ├── README.md
│   ├── requirements.txt
│   └── serviceAccountKey.json
├── frontend/
│   ├── dist/
│   ├── node_modules/
│   ├── public/
│   ├── src/
│   ├── .env
│   ├── .eslintrc.cjs
│   ├── .firebaserc
│   ├── .gitignore
│   ├── firebase.json
│   ├── index.html
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   └── vite.config.js
├── .firebaserc
├── .gitignore
├── firebase_config.copy.py
└── README.md
</pre>

- **`backend/`**: Contém todos os arquivos relacionados ao backend.
  - **`Images/`**: Pasta para armazenamento de imagens.
  - **`Resources/`**: Pasta para recursos adicionais.
  - **`app.py`**: Script principal que executa a API do backend.
  - **`encodeFile.p`**: Arquivo com codificações de rostos previamente conhecidas.
  - **`firebase_config.py`**: Configuração do Firebase.
  - **`requirements.txt`**: Arquivo com as dependências do backend.
  - **`serviceAccountKey.json`**: Chave de conta de serviço para o Firebase.

- **`frontend/`**: Contém todos os arquivos relacionados ao frontend.
  - **`src/`**: Código fonte do frontend.
  - **`index.html`**: Arquivo HTML principal.
  - **`vite.config.js`**: Configuração do Vite.
  - **`package.json`**: Gerenciamento de pacotes e dependências do frontend.

### Requisitos

- **Python 3.6+**
- **Node.js e npm**

#### Bibliotecas Backend:

- `opencv-python`
- `face_recognition`
- `numpy`
- `flask`
- `firebase-admin`

#### Dependências Frontend:

- `vite`
- `react`
- `firebase`

### Instalação (local)

#### Backend

1. Clone o repositório:

    ```bash
    git clone https://github.com/usuario/face-recognition-auth.git
    ```

2. Navegue para o diretório do backend:

    ```bash
    cd face-recognition-auth/backend
    ```

3. Crie um ambiente virtual e ative-o:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

4. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

5. Execute o script principal:

    ```bash
    python app.py
    ```

#### Frontend

1. Navegue para o diretório do frontend:

    ```bash
    cd ../frontend
    ```

2. Instale as dependências:

    ```bash
    npm install
    ```

3. Execute o servidor de desenvolvimento:

    ```bash
    npm run dev
    ```

### Uso

1. Certifique-se de que sua webcam está conectada.
2. Execute o backend conforme descrito acima.
3. Execute o frontend conforme descrito acima.
4. Acesse o sistema através do navegador na URL fornecida pelo Vite.

### Personalização

- Para adicionar mais imagens de usuários, coloque as novas imagens na pasta `backend/Images`. [OUTDATED]
- Para adicionar mais imagens de usuários entre nesse [link](https://face-recognition-auth-92ac0.firebaseapp.com/).
- As codificações de rostos são carregadas a partir do arquivo `encodeFile.p`. Você pode atualizar este arquivo com novas codificações conforme necessário.

### Notas Importantes

- Certifique-se de que o arquivo `.env` contém as variáveis de ambiente necessárias para a configuração do Firebase. Se você estiver em um ambiente de desenvolvimento, você pode criar um arquivo `.env` com o seguinte conteúdo:

    ```env
    FIREBASE_API_KEY=YOUR_FIREBASE_API_KEY
    FIREBASE_AUTH_DOMAIN=YOUR_FIREBASE_AUTH_DOMAIN
    FIREBASE_PROJECT_ID=YOUR_FIREBASE_PROJECT_ID
    FIREBASE_STORAGE_BUCKET=YOUR_FIREBASE_STORAGE_BUCKET
    FIREBASE_MESSAGING_SENDER_ID=YOUR_FIREBASE_MESSAGING_SENDER_ID
    FIREBASE_APP_ID=YOUR_FIREBASE_APP_ID
    ```

- O backend está configurado para escutar alterações na coleção `Person` do Firebase e atualizar as codificações de rostos automaticamente.

### Atualizações Recentes

- **Backend**:
  - Adicionada a funcionalidade de registrar a data e hora de autenticação com o campo `autenticado_em`.
  - A resposta da API agora inclui `autenticado_em` com a data e hora da autenticação.

- **Frontend**:
  - Atualizado para exibir o campo `autenticado_em` com a data e hora da autenticação.

### Exemplo de Resposta da API

```json
[
  {
    "id": "user1",
    "email": "user1@example.com",
    "name": "User One",
    "location": [0, 0, 100, 100],
    "autenticado_em": "2024-07-11 15:45:30"
  }
]
