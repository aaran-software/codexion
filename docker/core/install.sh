#!/bin/bash

echo "🧼 Shutting down existing container..."
docker compose -f docker/core/cortex.yml down --remove-orphans

echo "🧹 Removing old image..."
docker rmi -f cortex-app:v1 || true

echo "🔨 Rebuilding image..."
docker build -t cortex-app:v1 -f docker/core/Dockerfile .

echo "🚀 Starting services..."
docker compose -f docker/core/cortex.yml up -d
