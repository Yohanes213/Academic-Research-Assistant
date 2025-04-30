FROM python:3.10-slim

WORKDIR /app
# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5001

# Use uvicorn to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]