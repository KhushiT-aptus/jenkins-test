# Use official Python base image
FROM python:3.10.16-slim

# Create a non-root user
RUN useradd -m jenkin-user

# Set working directory
WORKDIR /app

# Copy requirement files
COPY requirements.txt .

# Install dependencies (as root)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY main.py .

# Switch to non-root user
USER jenkin-user

# Expose port
EXPOSE 8000

# Run FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
