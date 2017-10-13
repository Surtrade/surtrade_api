# Surtrade API

## Requirements
- To create requirements.txt type "pip freeze > requirements.txt"
- To install requirements type: pip install -r requirements.txt

## Environment
- To activate environment type in terminal "source .env"

## Server
- To start server type "flask run"

## Local Tunnel
- type  "lt --port 5000 --subdomain surtrade"

## Linux
### Processes
- To see the processes is ps ax|grep gunicorn and to stop gunicorn_django is pkill gunicorn
### Gunicorn
- To open the 5000 port type "sudo ufw allow 5000"
- To run server type "python run.py"
- To set it up type "gunicorn --bind 0.0.0.0:5000 wsgi:app"

## PostgreSQL 
**[Get Started](https://www.codementor.io/devops/tutorial/getting-started-postgresql-server-mac-osx)**
- Create a role
- Create a database

## SQLAlchemy
- To generate database type "python manage.py db init"
- To migrate the data type "python manage.py db migrate"
- To apply the data type "python manage.py db upgrade"

### CREATE / DROP
- CREATE ROLE myrole;
- DROP ROLE myrole;
- CREATE DATABASER mydatabase;
- DROP DATABASER mydatabase;

### Access
###### Using admin role
- GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

###### Using admin role connected to mydatabase after migration
- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;
- GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO myuser;

## GIT
- git remote add origin  <REMOTE_URL> 