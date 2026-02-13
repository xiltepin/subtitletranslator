FROM python:3.11-slim

WORKDIR /app

# system deps (optional but safe)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# copy backend code
COPY . .

# install python deps
RUN pip install --no-cache-dir flask flask-cors

EXPOSE 5001

CMD ["python", "app.py"]
