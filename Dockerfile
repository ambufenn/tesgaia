# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install deps dulu (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode
COPY . .

# Port Cloud Run
ENV PORT=8080

# Jalankan Streamlit
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
