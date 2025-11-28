FROM python:3.11-slim

# Create app directory
WORKDIR /app

# Install runtime dependencies
COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend ./backend

# Expose default port for uvicorn
EXPOSE 8000

# Default command (can be overridden in docker run)
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
