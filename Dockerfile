# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

#RUN apk add --no-cache gcc musl-dev linux-headers

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

CMD [ "python3", "flask", "run" ]