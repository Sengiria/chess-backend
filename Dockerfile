# Use official lightweight Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and stockfish binary
COPY app ./app
COPY stockfish ./stockfish

# Make Stockfish executable
RUN chmod +x ./stockfish

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Run FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
