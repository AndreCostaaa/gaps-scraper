
FROM python:3.10-alpine

# copy files
COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

#cron
RUN echo '*/5  *  *  *  * python3 /app/main.py' >> /var/spool/cron/crontabs/root
RUN echo '*/30  *  *  *  * python3 /app/fetch_next_schedule' >> /var/spool/cron/crontabs/root
# RUN echo '*/5  *  *  *  * python3 /app/fetch_prov_bulletin.py' >> /var/spool/cron/crontabs/root
CMD ["crond", "-f"]
