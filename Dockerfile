# Use official Python base image
FROM python:3.10.16-slim

# Set working directory
WORKDIR /app

# Copy requirement files first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI app code
COPY main.py .

# Expose port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
