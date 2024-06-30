# Use uma imagem base oficial do Ubuntu
FROM ubuntu:20.04

# Definir variáveis de ambiente para evitar prompts durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualizar e instalar dependências do sistema necessárias para compilar bibliotecas
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3-pip \
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
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho
WORKDIR /app

# Atualizar o pip e instalar cmake
RUN python3.11 -m pip install --upgrade pip
RUN pip install cmake

# Instalar dlib separadamente com suas dependências
RUN pip install dlib==19.24.0

# Copiar os arquivos de requirements e instalar as dependências do Python
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python3.11", "backend/app.py"]
