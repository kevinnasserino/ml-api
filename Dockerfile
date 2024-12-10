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

# Ekspose port 8080
EXPOSE 8080

# Jalankan aplikasi Flask
CMD ["python", "-m", "app"]
