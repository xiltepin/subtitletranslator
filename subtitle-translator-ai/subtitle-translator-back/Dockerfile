FROM python:3.11-slim
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY . .

# Install Python dependencies (added tqdm and requests for subtitle_translator.py)
RUN pip install --no-cache-dir flask flask-cors openai requests tqdm

# Make translate.sh executable
RUN chmod +x translate.sh

EXPOSE 5001
CMD ["python", "app.py"]
