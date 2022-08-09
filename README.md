# Overview

This repo contains a list of the components for the exam for the Backend Software Engineer position at Array, as outlined [here](https://gitlab.com/array.com/tests-backend). This guide has been written for users using Ubuntu 20.04 LTS.


# Design

This application creates a basic user registration and authentication application using **Flask** as a framework. **WTForms** is used specifically for the validation of username and password fields, and **Bcrypt** for password hashing (which avoids storing passwords in plain text). I also decided to use **SQLAlchemy** as an ORM for interaction between the Python classes and **PostgreSQL** data tables, automatically converting function calls within the Flask app to SQL statements to the database.


## Getting started

Make sure that you have a GitHub account with valid SSH keys. Also make sure you have Docker and PostgreSQL installed [Docker](https://docs.docker.com/engine/installation/) [PostgreSQL](https://www.postgresql.org/download/) and run the following in a terminal:

```shell
git clone git@github.com:blackgwehnade/flask_authy_docker_app.

cd <__wheredidyouclonetherepo__>/flask_authy_docker_app

docker-compose up
```

Otherwise, for the standalone web service:

```shell
pip install -r requirements.txt
python app/app.py
```

The Flask app and PostgreSQL database should now be up and running


# PostgreSQL steps

After you have started the Flask app using Docker Compose, you will need to make sure that the PostgreSQL database is working properly. Run the following command in a separate (split) terminal.

```shell
psql -h localhost -p 5436 -U postgres -d users
```

Provide the password: *default_pw* when prompted.

# Using the app

Now you should be able to start registering and logging in users.
First visit [http://localhost:4000](http://localhost:4000) and click on *Register Page*. Then enter in a new username of at least 8 alphanumeric characters and then a password of 8-20 characters.

(Note: if you already have a local process running on Port 4000, you will either have to halt it or change the port number in *app.py*, *DOCKERFILE* and *docker-compose.yaml*.

# Example

Currently we have no registered users in the database, and thus when we make a SQL query to the DB as outlined below we'll get no results. 

```shell
users=# SELECT * FROM user;
id | username | password 
----+----------+----------
(0 rows)
```

In this example, I will create two users, **Damian** and **Janessa** and assign them the passwords *DamianPW* and *JanessaPW* respectively. Then let's run the ```SELECT * FROM public.user;``` command again and validate the new entries.

```shell
id | username |                                                          password                                                          
----+----------+----------------------------------------------------------------------------------------------------------------------------
  1 | Damian   | \x243262243132246f42612f644d3342734c486d7847494878724e6751655a63706c72767766714f586f62483254766258516a2f3035454a6657334671
  2 | Janessa  | \x243262243132244131556d2e6a4e68443866754b7a5a30764e7556762e3050683953433656735173694d74336a54516777755a7665486e4539657a53
(2 rows)
```
We can now confirm that our app works, with the usernames and corresponding hashed passwords that were created using the BCrypt module (you should never see the passwords stored in plain text).

# Logging in and out

Finally, let's visit the [http://localhost:4000/login](http://localhost:4000/login) endpoint and login in with any valid username/password credential. Once we've done so, we should be redirected to [http://localhost:4000/dashboard](http://localhost:4000/dashboard). Click on the **Click here to logout.** button to return back to the homage page. You should no longer be able to visit the dashboard endpoint since you are logged out.
