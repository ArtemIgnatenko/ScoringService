#!/bin/bash

# Создаем директории для Docker
mkdir -p docker

# Копируем Dockerfile для API и UI
cp -f Dockerfile.api docker/
cp -f Dockerfile.ui docker/

# Запускаем Docker Compose
docker-compose up -d

echo "ML Billing Service запущен!"
echo "API доступен по адресу: http://localhost:8000/api/docs"
echo "UI доступен по адресу: http://localhost:8501"