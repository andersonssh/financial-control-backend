FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip --break-system-packages && pip install --no-cache-dir -r requirements.txt --break-system-packages
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
