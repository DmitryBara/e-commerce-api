FROM python:3.8.3-alpine

WORKDIR /app

EXPOSE 8000

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .