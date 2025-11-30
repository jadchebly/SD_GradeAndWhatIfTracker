FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install backend dependencies first (better caching)
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Copy frontend (static files)
COPY frontend ./frontend

# Expose port
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]

