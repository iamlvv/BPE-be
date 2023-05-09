FROM python:alpine3.16 as bpsky-be-image

COPY requirements.txt .

RUN pip install -r ./requirements.txt

RUN pip install Flask twilio
