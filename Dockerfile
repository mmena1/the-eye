FROM python:3.9-slim
RUN groupadd dev && useradd -m dev -g dev
USER dev
WORKDIR /home/dev/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-warn-script-location
COPY consumer_affairs consumer_affairs
COPY the_eye the_eye
COPY manage.py ./
