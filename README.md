# Gaps Scraper

This is a python (selenium) webscraping project that scrapes Gaps @ HEIG-VD.

It currently fetches grades and schedule changes. It uses e-mail notifications to notify the user.

## Requirements to run

Docker

## Requirements to develop

Install all requirements

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

And change the create_driver function to create the driver of your choosing for your developement.

To make sure it works when packaging into the docker image, don't forget to revert your changes:

```python 
def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.BinaryLocation = "/usr/bin/chromium-browser"

    driver_path = "/usr/bin/chromedriver"
    service = Service(driver_path)
    driver = webdriver.Chrome(options=options, service=service)
    return driver
```

## Docker

This program is easily packed into a docker image and deployed to a remote server (or a simple raspberry pi)

Inside the docker container, the script will be launched every 5 minutes and send e-mail notifications if there are any changes

## Configuration files

Two configurations files are needed

auth.json : Contains Gaps username and password

```json 
{
  "username": USERNAME WITHOUT @heig-vd.ch
  "password": PASSWORD
}
```

smtp_auth.json : Contains smtp auth information

Here's an  example using gmail's server to send the email notifications
```json
{
  "smtp_server": "smtp.gmail.com",
  "smtp_server_port": 465,
  "email_address": YOUR E-MAIL ADDRESS
  "email_token": YOUR APPLICATION TOKEN
}
```

## First usage

Clone this repository

`git clone https://github.com/AndreCostaaa/gaps-scraper.git`

Create your data directory

```
cd gaps-scraper
mkdir data
```
Create your authentication json files

```
cd data
touch auth.json
touch smtp_auth.json
nano/vim ...
```

Build and run

```
cd ..
docker compose up -d --build 
```

Feel free to notify me in case of any problems or if you'd like to add some features :D


