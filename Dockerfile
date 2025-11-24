# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy app and requirements
COPY main.py .
COPY src/ src/

# Install dependencies
RUN pip install flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
