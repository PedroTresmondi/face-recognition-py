#!/bin/bash

echo "Instalando dependências do Python"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Falha na instalação das dependências"
    exit 1
fi

echo "Iniciando a aplicação"
python3.8 backend/app.py
