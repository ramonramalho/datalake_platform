#!/bin/bash

# Atualize os pacotes
sudo apt-get update -y

# Instale o Docker
sudo apt-get install -y docker.io

# Adicione o usuário 'ubuntu' ao grupo 'docker' para permitir rodar Docker sem sudo
sudo usermod -aG docker ubuntu

# Instale o Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.14.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crie um diretório para o Airflow
mkdir -p ~/airflow

# Entre no diretório
cd ~/airflow

# Crie o arquivo docker-compose.yaml para o Airflow
cat <<EOF > docker-compose.yaml
version: '3'
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
  airflow-init:
    image: apache/airflow:2.4.3
    depends_on:
      - postgres
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
      AIRFLOW__CORE__FERNET_KEY: $(openssl rand -base64 32)
      AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
      AIRFLOW__WEBSERVER__SECRET_KEY: $(openssl rand -base64 32)
    command: bash -c "airflow db init"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
  webserver:
    image: apache/airflow:2.4.3
    depends_on:
      - postgres
      - airflow-init
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    ports:
      - "8080:8080"
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: bash -c "airflow webserver"
  scheduler:
    image: apache/airflow:2.4.3
    depends_on:
      - webserver
    environment:
      AIRFLOW__CORE__EXECUTOR: LocalExecutor
      AIRFLOW__CORE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    volumes:
      - ./dags:/opt/airflow/dags
      - ./logs:/opt/airflow/logs
      - ./plugins:/opt/airflow/plugins
    command: bash -c "airflow scheduler"
volumes:
  postgres-db-volume:
EOF

# Inicie os serviços do Airflow
sudo docker-compose up -d

# Exibir o status dos serviços
sudo docker-compose ps
