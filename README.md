# Foodgram

Project Foodgram is a platform for collecting recipes. Users can save their own recipes or browse recipes, created by other users. Also they can save favourite recipes, save recipes for creatinf shopping list. All recipes can be filtered by tags.
## Getting Started

The project will be tested and deployed to your server via Github Actions after you push it to your git repository.

### Prerequisites

To run this project on your server you need to add following [git secrets](https://docs.github.com/en/actions/reference/encrypted-secrets) to your repository:
DOCKER_USER, DOCKER_PASSWORD - username and password of your docker account
HOST, USER, SSH_KEY, PASSPHRASE (optional) - server public ip, username used to connect to server, private id_rsa key and passphrase for id_rsa key (if needed)
TELEGRAM_TO, TELEGRAM_TOKEN - ID of your telegram account and token of your telegram bot (if you wish to recieve message about completed workflow)

In case of forgotten password, user can restore it with the help of email restore form. Link for email restore will be send to email address that was used to register. 
To be able to send password restore links, change .env variables, EMAIL_HOST_USER and EMAIL_HOST_PASSWORD to your email and host password for sending emails.

There is an example .env file named .env.example. Rename it to .env and change values of variables for work with database if needed.
Also you will need server and CLI to connect to your server via SSH. 

### Installing

After github workflow is complete execute following commands via CLI from home directory on your server

To get into app container
```
sudo docker exec -it foodgram_web_1 bash
```
From there you will be able to create database
```
python manage.py makemigrations
python manage.py migrate
```
To create superuser (you will be asked information required for user registration)
```
python manage.py createsuperuser
```
To collect static
```
python manage.py collectstatic
```
To apply fixtures (must-do for proper work with ingredients and tags)
```
python manage.py loaddata fixtures.json
```
The app will be available at your server ip address.

## Built With

* [Django](https://www.djangoproject.com) - The web framework used
* [Postgres](https://www.postgresql.org) - The database system used
* [Docker](https://www.docker.com) - Tool used to containerize and run up application
