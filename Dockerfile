FROM python:3.12-slim

WORKDIR /app

# Copy all code from src/ folder into /app
COPY src/ .

# Install dependencies
RUN pip install flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
