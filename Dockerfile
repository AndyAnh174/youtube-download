FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Collect static files
# We set SECRET_KEY dummy value for build phase because django check checks it
RUN python manage.py collectstatic --noinput --clear

# Expose port
EXPOSE 8000

# Create media directory
RUN mkdir -p media/downloads

# Run with Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
