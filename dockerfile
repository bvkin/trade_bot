FROM python:3.9

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app

CMD ["python", "app.py"]