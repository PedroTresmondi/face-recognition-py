<h1>⚠️WIP⚠️</h1>
<h2>Face Recognition Authentication System</h2>

<h3>Descrição do Projeto</h3>
<p>Este projeto é um sistema de autenticação facial que utiliza a webcam para detectar e reconhecer rostos, autenticando usuários com base em suas características faciais. O backend é desenvolvido em Python e está em deploy no Fly.io, permitindo que a autenticação funcione sem a necessidade de rodar o backend localmente. O frontend é desenvolvido com Vite.</p>

<h3>Funcionalidades</h3>
<ul>
  <li>Captura de vídeo em tempo real através da webcam.</li>
  <li>Detecção e reconhecimento de rostos no quadro de vídeo.</li>
  <li>Codificação e comparação de rostos utilizando a biblioteca <code>face_recognition</code>.</li>
  <li>Interface de usuário interativa desenvolvida com Vite.</li>
  <li>Integração com Firebase para armazenamento e autenticação de dados.</li>
</ul>

<h3>Estrutura de Arquivos</h3>
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
<ul>
  <li><code>backend/</code>: Contém todos os arquivos relacionados ao backend.</li>
  <ul>
    <li><code>Images/</code>: Pasta para armazenamento de imagens.</li>
    <li><code>Resources/</code>: Pasta para recursos adicionais.</li>
    <li><code>app.py</code>: Script principal que executa a API do backend.</li>
    <li><code>encodeFile.p</code>: Arquivo com codificações de rostos previamente conhecidas.</li>
    <li><code>firebase_config.py</code>: Configuração do Firebase.</li>
    <li><code>requirements.txt</code>: Arquivo com as dependências do backend.</li>
    <li><code>serviceAccountKey.json</code>: Chave de conta de serviço para o Firebase.</li>
  </ul>
  <li><code>frontend/</code>: Contém todos os arquivos relacionados ao frontend.</li>
  <ul>
    <li><code>src/</code>: Código fonte do frontend.</li>
    <li><code>index.html</code>: Arquivo HTML principal.</li>
    <li><code>vite.config.js</code>: Configuração do Vite.</li>
    <li><code>package.json</code>: Gerenciamento de pacotes e dependências do frontend.</li>
  </ul>
</ul>

<h3>Requisitos</h3>
<ul>
  <li><strong>Python 3.6+</strong></li>
  <li><strong>Node.js e npm</strong></li>
</ul>

<h4>Bibliotecas Backend:</h4>
<ul>
  <li><code>opencv-python</code></li>
  <li><code>face_recognition</code></li>
  <li><code>numpy</code></li>
  <li><code>flask</code></li>
  <li><code>firebase-admin</code></li>
</ul>

<h4>Dependências Frontend:</h4>
<ul>
  <li><code>vite</code></li>
  <li><code>react</code></li>
  <li><code>firebase</code></li>
</ul>

<h3>Instalação (local)</h3>

<h4>Backend</h4>
<ol>
  <li>Clone o repositório:
    <pre><code>git clone https://github.com/usuario/face-recognition-auth.git</code></pre>
  </li>
  <li>Navegue para o diretório do backend:
    <pre><code>cd face-recognition-auth/backend</code></pre>
  </li>
  <li>Crie um ambiente virtual e ative-o:
    <pre><code>python -m venv venv
source venv/bin/activate  # No Windows use `venv\Scripts\activate`</code></pre>
  </li>
  <li>Instale as dependências:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  <li>Execute o script principal:
    <pre><code>python app.py</code></pre>
  </li>
</ol>

<h4>Frontend</h4>
<ol>
  <li>Navegue para o diretório do frontend:
    <pre><code>cd ../frontend</code></pre>
  </li>
  <li>Instale as dependências:
    <pre><code>npm install</code></pre>
  </li>
  <li>Execute o servidor de desenvolvimento:
    <pre><code>npm run dev</code></pre>
  </li>
</ol>

<h3>Uso</h3>
<ol>
  <li>Certifique-se de que sua webcam está conectada.</li>
  <li>Execute o backend conforme descrito acima.</li>
  <li>Execute o frontend conforme descrito acima.</li>
  <li>Acesse o sistema através do navegador na URL fornecida pelo Vite.</li>
</ol>

<h3>Personalização</h3>
<ul>
  <li>Para adicionar mais imagens de usuários, coloque as novas imagens na pasta <code>backend/Images</code>. [OUTDATED]</li>
  <li>Para adicionar mais imagens de usuários entre nesse <a href="https://face-recognition-auth-92ac0.firebaseapp.com/">link</a>.</li>
  <li>As codificações de rostos são carregadas a partir do arquivo <code>encodeFile.p</code>. Você pode atualizar este arquivo com novas codificações conforme necessário.</li>
</ul>

<h3>Notas Importantes</h3>
<ul>
  <li>Para o sistema funcionar corretamente, o frontend precisa ser executado localmente.</li>
  <li>A autenticação no backend em Python está no Fly.io e só permite requisições do <code>localhost:5173</code> (front local).</li>
  <li>Para ser autenticado, o usuário precisa se cadastrar primeiro.</li>
</ul>
