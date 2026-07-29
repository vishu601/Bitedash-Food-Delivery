# Python ka official image use karenge
FROM python:3.14-slim

# Working directory set karo
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies install karo (agar database ya build ke liye chahiye ho)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Requirements file copy karke dependencies install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Poora project copy karo
COPY . .

# Static files collect karo aur migrations run karne ke liye script ya command
# (Hum ise docker-compose se handle karenge)

# Port expose karo
EXPOSE 8000

# Server run karne ki command (Daphne / Gunicorn ya Runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
