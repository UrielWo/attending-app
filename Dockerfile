# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR /app 

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ./.env

ENTRYPOINT ["python3", "myFlask.py"]	
