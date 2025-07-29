FROM python:3.12-slim AS cortex

LABEL maintainer="cortex"
LABEL author="Sundar <sundar@sundar.com>"
LABEL version="1.0"
LABEL description="cortex - Dev image for Python FastAPI + React + Vite development"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    PATH="/home/devops/.local/bin:$PATH" \
    MODE=dev \
    PYTHONPATH="/home/devops/codexion"

# Create user
RUN useradd -m -s /bin/bash devops && echo "devops:sundar" | chpasswd

# Install system deps + Node.js (v22) and tools
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y sudo curl git build-essential libpq-dev gnupg ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn vite concurrently && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER devops
WORKDIR /home/devops

# Clone repo
RUN git clone --depth 1 https://github.com/AARAN-SOFTWARE/codexion.git

WORKDIR /home/devops/codexion

# Create shared folder (prevents volume issues)
RUN mkdir -p shared

# Install backend and frontend deps
RUN pip install --no-cache-dir -r requirements.txt && npm install

# Prebuild frontend in prod
RUN if [ "$MODE" = "prod" ]; then npm run build; fi

# Expose backend (4000) and frontend (3000) ports
EXPOSE 4001 3001

# Run backend + frontend dev or prod
CMD bash -c "\
  if [ \"$MODE\" = \"prod\" ]; then \
    echo 'Starting FastAPI backend in production...'; \
    gunicorn cortex.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:4001 -w 4 --timeout 60; \
  else \
    echo 'Starting frontend (port 3000) and backend (port 4001)...'; \
    concurrently \
      \"uvicorn cortex.main:app --host 0.0.0.0 --port 4001 --reload\" \
      \"npm run dev -- --host 0.0.0.0\"; \
  fi"
