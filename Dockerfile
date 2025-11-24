# ======== STAGE 1: BUILDER ========
FROM python:3.12-slim AS builder

# Diretório de trabalho dentro do container
WORKDIR /app

# Atualiza pip
RUN pip install --no-cache-dir --upgrade pip

# Copia apenas o requirements primeiro (melhora cache de build)
COPY requirements.txt .

# Instala dependências em um prefixo separado (/install)
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ======== STAGE 2: RUNTIME ========
FROM python:3.12-slim

# Deixa o Python não bufferizar logs (melhor em containers)
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia as libs já instaladas no builder para a imagem final
COPY --from=builder /install /usr/local

# Copia somente o código da app
COPY app ./app

# Porta que o Uvicorn usa
EXPOSE 8000

# Comando para subir sua API FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
