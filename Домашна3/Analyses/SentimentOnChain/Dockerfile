FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV TRANSFORMERS_NO_TF=1
ENV TOKENIZERS_PARALLELISM=false
ENV HF_HOME=/app/.hf

EXPOSE 8003

CMD ["uvicorn", "sentiment_api:app", "--host", "0.0.0.0", "--port", "8003"]
