# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip &&     pip install -r requirements.txt

# Default command
CMD ["bash", "scripts/scheduler.sh"]
