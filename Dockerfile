FROM python:3.8-slim

# Definir variáveis de ambiente para evitar prompts durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema necessárias para compilar bibliotecas
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    make \
    libboost-python-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libboost-filesystem-dev \
    libboost-serialization-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libopenblas-dev \
    liblapack-dev \
    wget \
    zlib1g-dev \
    libsm6 \
    libxext6 \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Atualizar o pip, instalar cmake e wheel primeiro
RUN pip install --upgrade pip \
    && pip install wheel setuptools \
    && pip install dlib==19.24.0

# Copiar os arquivos de requirements e instalar as dependências do Python
COPY backend/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copiar o restante dos arquivos do projeto
COPY backend/ /app/

COPY backend/firebase_credentials.json /app/firebase_credentials.json

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
