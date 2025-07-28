# Stage 1: Build React frontend
FROM node:20 AS frontend-builder
WORKDIR /app
COPY package.json package-lock.json ./
COPY resources/ ./resources/
RUN npm install
RUN npm run build --prefix ./resources

# Stage 2: Build Python backend
FROM python:3.11-slim AS backend
WORKDIR /app

# Copy backend files
COPY cortex/ ./cortex/
COPY apps/ ./apps/
COPY config/ ./config/
COPY database/ ./database/
COPY framework/ ./framework/
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy React build output
COPY --from=frontend-builder /app/resources/dist/ ./dist/

# Copy package.json for reference (optional)
COPY package.json ./

# Set up environment file
COPY .env.sample .env

# Expose the backend port
EXPOSE 4000

# Set default command
CMD ["python", "cortex/main.py"]
