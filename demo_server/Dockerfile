FROM python:3.11-slim

WORKDIR /app

COPY demo_server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY demo_server/app.py .

EXPOSE 5000

CMD ["python", "app.py"]
