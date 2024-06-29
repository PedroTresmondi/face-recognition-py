import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, storage, db

load_dotenv()

cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
print(f"Caminho do arquivo de credenciais: {cred_path}")

database_url = os.getenv('FIREBASE_DATABASE_URL')
storage_bucket = os.getenv('FIREBASE_STORAGE_BUCKET')

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': database_url,
    'storageBucket': storage_bucket
})

