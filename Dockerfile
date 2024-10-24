FROM python:3.10.6-slim-bullseye

WORKDIR /tmp

RUN apt update
RUN apt upgrade -y
RUN apt install -y curl
RUN apt install -y git
RUN apt clean -y

RUN pip install --no-cache-dir --upgrade pip

COPY . .
RUN pip install .

CMD uvicorn redis_app.app:app --host $HOST --port $API_PORT --reload
