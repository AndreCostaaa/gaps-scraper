FROM python:3.10-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver
RUN PATH="/usr/bin/chromedriver:${PATH}"
# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium==4.4.3
RUN pip install webdriver_manager

COPY . /src
WORKDIR /src
#cron
RUN echo '*/5  *  *  *  * python3 /src/main.py' >> /var/spool/cron/crontabs/root

CMD crond -f
