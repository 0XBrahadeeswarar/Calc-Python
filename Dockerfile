# Use official Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy all application code from src/ into /app
COPY src/ .  # copies main.py and other src files into /app/

# Install dependencies
RUN pip install flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
