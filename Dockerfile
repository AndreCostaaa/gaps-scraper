
FROM python:3.10-alpine

# copy files
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

#cron
RUN echo '*/5  *  *  *  * python3 /app/main.py' >> /var/spool/cron/crontabs/root
CMD ["crond", "-f"]
