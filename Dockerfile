FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install gunicorn

WORKDIR /app

# Copie du code source
COPY . .

# Installation des dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt
# RUN python manage.py makemigrations

RUN python manage.py collectstatic --noinput

COPY startup.sh /app/
RUN chmod +x /app/startup.sh

# Exposition du port
EXPOSE 8000
