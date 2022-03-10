FROM python:3.9-alpine
WORKDIR /data
RUN pip install bs4
RUN pip install requests



