FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

CMD ["gunicorn", "--bind", "0.0.0.0:9100", "core.wsgi:application"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "core.wsgi:application"]