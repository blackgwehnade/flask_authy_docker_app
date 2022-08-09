# Overview

This repo contains a list of the components for the exam for the Backend Software Engineer position at Array, as outlined [here](https://gitlab.com/array.com/tests-backend). This guide has been written for users using Ubuntu 20.04 LTS.


# flask-app

This application creates a basic user registration and authentication application using Flask as a framework. User and corresponding passwords are saved on a PostgreSQL database, with the schema outlined below.


## Getting started

Make sure that you have a GitHub account with valid SSH keys. Also make sure you have Docker and PostgreSQL installed [Docker](https://docs.docker.com/engine/installation/) [PostgreSQL](https://www.postgresql.org/download/) and run the following in a terminal:

```shell
git clone git@github.com:blackgwehnade/flask_authy_docker_app.

cd (__yourpath__)/flask_authy_docker_app

docker-compose up
```

Otherwise, for the standalone web service:

```shell
pip install -r requirements.txt
python app/app.py
```

The Flask app and PostgreSQL database should now be up and running


# PostgreSQL

After you have started the Flask app using Docker Compose, you will need to make sure that the PostgreSQL database is working properly. Run the following command in a separate (split) terminal.

```shell
psql -h localhost -p 5436 -U postgres -d users
```

Provide the password: *default_pw* when prompted.

# Using the app

Now you should be able to start registering and logging in users.
First visit [http://localhost:4000](http://localhost:4000) and click on *Register Page*. Then enter in a new username of at least 8 alphanumeric characters and then a password of 8-20 characters.

(Note: if you already have a local process running on Port 4000, you will either have to halt it or change the port number in *app.py*, *DOCKERFILE* and *docker-compose.yaml*.
