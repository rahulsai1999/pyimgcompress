FROM python:3.7.3-slim
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn","-b","0.0.0.0:8000","app:app"]