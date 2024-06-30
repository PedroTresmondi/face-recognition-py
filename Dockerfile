# Use uma imagem base oficial do Ubuntu
FROM ubuntu:20.04

# Definir variáveis de ambiente para evitar prompts durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependências do sistema necessárias para compilar bibliotecas
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-dev \
    python3-pip \
    python3-distutils \
    python3-setuptools \
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
RUN python3.8 -m pip install --upgrade pip
RUN pip install wheel cmake

# Instalar dlib diretamente
RUN pip install dlib==19.24.0

# Copiar os arquivos de requirements e instalar as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python3.8", "backend/app.py"]
