FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./backend/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install django-eventstream
COPY ./backend/ /app