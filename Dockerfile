FROM python:3.10-slim

EXPOSE 8000

# Installer les dépendances système requises pour psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    # libpq-dev includes pg_config lib necessary for psycopg2
    libpq-dev \     
    gcc  \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy the project inside the container
COPY . /app

# install necessary packages
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
#sqlite3 is for the database --> now changed to PostgreSQL
RUN apt update && apt install sudo && sudo apt install sqlite3

# starting the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]