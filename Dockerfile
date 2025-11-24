FROM python:3.12-slim

WORKDIR /app


COPY src/ .


RUN pip install flask

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["python", "main.py"]
