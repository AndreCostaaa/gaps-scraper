# Gaps Scraper

This is a python webscraping project that scrapes Gaps @ HEIG-VD.

It currently fetches grades and schedule changes. It uses e-mail notifications and interfaces with [gaps-notfiier-api](https://github.com/AndreCostaaa/gaps-notifier-api) to notify the user.

## Requirements to run

Docker

## Requirements to develop

Install all requirements

```shell
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

And Have Fun !

## Docker

This program is easily packed into a docker image and deployed to a remote server (or a simple raspberry pi)

Inside the docker container, the script will be launched every 5 minutes and send notifications if there are any changes

## Configuration files

Env variables are used to configure the program

```env
GAPS_USERNAME=<gaps username without @heig-vd.ch>
GAPS_PASSWORD=<gaps password>

#Gaps Notifier
GAPS_NOTIFIER_URL=<gaps notifier base url> # eg: https://gaps-notifier.lutonite.dev/
GAPS_NOTIFIER_USER_ID=<gaps notifier user id>

#Email Notifications
SMTP_SERVER=<smtp server>
SMTP_PORT=<smtp port>
EMAIL_ADDRESS=<smtp login email>
EMAIL_TOKEN=<smtp login token>
```

### SMTP Configuration example

Here's an example using a gmail account

```env
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=465
EMAIL_ADDRESS= <your email>
EMAIL_TOKEN= <application token>
```

## First usage

1. Clone this repository

```shell
git clone https://github.com/AndreCostaaa/gaps-scraper.git
```

2. Modify the [skeleton.env](./skeleton.env) file with the necessary information

```shell
nano/vi skeleton.env
```

3. Rename the file to .env

```shell
mv skeleton.env .env
```

4. Build and Run

```shell
docker compose up -d --build
```

Feel free to notify me in case of any problems or if you'd like to add some features :D
