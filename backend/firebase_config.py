import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage, db

load_dotenv()

# Carregar o caminho do JSON das variáveis de ambiente
#cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')

# Inicializar credenciais do Firebase
cred = credentials.Certificate('firebase_credentials.json') 
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
})
