FROM python:3.8.0b1-slim
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn","app:app"]