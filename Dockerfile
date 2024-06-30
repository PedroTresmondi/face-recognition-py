# Use uma imagem base oficial do Python que inclui ferramentas de construção
FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

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
    && rm -rf /var/lib/apt/lists/*

# Verificar a instalação do cmake
RUN cmake --version

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requirements e instalar as dependências
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install cmake
RUN pip install -r requirements.txt

# Copiar o restante dos arquivos do projeto
COPY . .

# Expor a porta que o Flask usará
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "backend/app.py"]
