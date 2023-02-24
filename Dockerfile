FROM python:3.10-alpine

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.14/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.14/community" >> /etc/apk/repositories

# chromium and chromedriver
RUN apk update
RUN apk add chromium
RUN apk add chromium-chromedriver
RUN PATH="/usr/bin/chromedriver:${PATH}"

# upgrade pip
RUN pip install --upgrade pip

# install selenium
RUN pip install selenium==4.4.3

# copy files
COPY . /src
WORKDIR /src

# dumb-init
RUN apk add dumb-init
#RUN pip install dumb-init

ENTRYPOINT ["/usr/bin/dumb-init", "--"]

#cron
RUN echo '*/5  *  *  *  * python3 /src/main.py' >> /var/spool/cron/crontabs/root
CMD ["crond", "-f"]
