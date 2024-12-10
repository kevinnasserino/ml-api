# Gunakan base image Python
FROM python:3.9-slim

# Set work directory
WORKDIR /app

# Salin file requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode
COPY . .

# Set entrypoint Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
