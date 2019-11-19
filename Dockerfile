FROM python:3.7-buster

RUN adduser datagator

WORKDIR /home/datagator

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql


COPY app app
COPY migrations migrations
COPY index.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP index.py
RUN chown -R datagator:datagator ./
USER datagator

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]