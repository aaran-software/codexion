# Stage 1: Build React frontend
FROM node:22 AS frontend-builder

LABEL maintainer="cortex"
LABEL author="Sundar <sundar@sundar.com>"
LABEL version="1.0"
LABEL description="cortex - Custom image for Python FastAPI + React development"

WORKDIR /codexion

COPY package.json package-lock.json ./
COPY resources/ ./resources/

RUN npm install
#RUN #npm run build --prefix ./resources

# Stage 2: Build Python backend
FROM python:3.12-slim AS backend

# Create app directory
WORKDIR /codexion

# Set PYTHONPATH so cortex/ works as a module
ENV PYTHONPATH="/codexion"

# Copy backend files
COPY apps/ ./apps/
COPY sites/ ./sites/
COPY config/ ./config/
COPY cortex/ ./cortex/
COPY database/ ./database/
COPY prefiq/ ./prefiq/
COPY requirements.txt ./
COPY .env.sample .env
COPY package.json ./

# Copy React build output (optional: serve from /dist or backend)
COPY --from=frontend-builder /codexion/resources/dist/ ./dist/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose backend port
EXPOSE 4000

# Default entry
#CMD ["python", "cortex/main.py"]
