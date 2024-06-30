import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage, db

load_dotenv()

# Carregar JSON das variáveis de ambiente
cred_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
cred_dict = json.loads(cred_json)

# Inicializar credenciais do Firebase
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
})
    