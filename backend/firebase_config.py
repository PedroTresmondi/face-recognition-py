import os
import json
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage, db

load_dotenv()

# Obtenha o JSON da variável de ambiente
cred_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
if cred_json is None:
    raise ValueError("A variável de ambiente FIREBASE_CREDENTIALS_JSON não está definida")

# Parse o JSON
cred_dict = json.loads(cred_json)

# Inicialize as credenciais usando o dicionário JSON
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'databaseURL': os.getenv('FIREBASE_DATABASE_URL'),
    'storageBucket': os.getenv('FIREBASE_STORAGE_BUCKET')
})
