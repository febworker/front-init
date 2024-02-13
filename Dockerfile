FROM python:3.12.2

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY storage/data.json /app/storage/data.json

WORKDIR /app

CMD ["python", "main.py"]