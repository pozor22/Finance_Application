FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY finance_app /finance_app
WORKDIR /finance_app
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password finance_app-user

USER finance_app-user