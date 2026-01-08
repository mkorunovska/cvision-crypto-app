FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV HF_HOME=/app/.hf
ENV TOKENIZERS_PARALLELISM=false
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
ENV TF_CPP_MIN_LOG_LEVEL=2

EXPOSE 8001

CMD ["uvicorn", "technical_api:app", "--host", "0.0.0.0", "--port", "8001"]