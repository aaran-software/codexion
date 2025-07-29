FROM python:3.12 AS cortex

LABEL maintainer="cortex"
LABEL author="Sundar <sundar@sundar.com>"
LABEL version="1.0"
LABEL description="cortex - Dev image for Python FastAPI + React + Vite development"

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    sudo \
    curl \
    git \
    build-essential \
    libpq-dev \
    gnupg \
    ca-certificates && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js (v22) + npm
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && \
    apt-get install -y nodejs && \
    npm install -g yarn vite

# Create non-root user
RUN useradd -m -s /bin/bash devops && echo "devops:sundar" | chpasswd

# Switch to non-root user and set working dir
USER devops
WORKDIR /home/devops/codexion

# Set PYTHONPATH
ENV PYTHONPATH="/home/devops/codexion"

# Copy project files
COPY --chown=devops:devops apps/ ./apps/
COPY --chown=devops:devops sites/ ./sites/
COPY --chown=devops:devops config/ ./config/
COPY --chown=devops:devops cortex/ ./cortex/
COPY --chown=devops:devops database/ ./database/
COPY --chown=devops:devops prefiq/ ./prefiq/
COPY --chown=devops:devops .env.sample ./
COPY --chown=devops:devops LICENSE ./
COPY --chown=devops:devops package.json ./
COPY --chown=devops:devops postcss.config.js ./
COPY --chown=devops:devops pyproject.toml ./
COPY --chown=devops:devops README.md ./
COPY --chown=devops:devops requirements.txt ./
COPY --chown=devops:devops tailwind.config.js ./
COPY --chown=devops:devops tsconfig.app.json ./
COPY --chown=devops:devops tsconfig.json ./
COPY --chown=devops:devops tsconfig.node.json ./
COPY --chown=devops:devops vite.config.ts ./

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# Install Node packages
RUN npm install

# Expose FastAPI backend port
EXPOSE 4000

# Start backend
#CMD ["python", "cortex/main.py"]
