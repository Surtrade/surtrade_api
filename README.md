# Surtrade API

## 1 Setup
### 1.1 Install PostgreSQL Database
Tutorial MacOS:**[Get Started](https://www.codementor.io/devops/tutorial/getting-started-postgresql-server-mac-osx)**
Tutorial Ubuntu 16.04:**[Get Started](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-16-04)**

- Create a role
- Create a database
- Add privileges of database to role

#### 1.1.1 CREATE / DROP / ALTER
- CREATE ROLE myrole WITH LOGIN PASSWORD 'quoted password';
- DROP ROLE myrole;
- CREATE DATABASER mydatabase;
- DROP DATABASER mydatabase;
- ALTER ROLE myrole CREATEDB

#### 1.1.2 Access
##### 1.1.2.1 Using admin role
- GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;

##### 1.1.2.2 Using admin role connected to mydatabase after migration
- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO myuser;
- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO myuser;
- GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO myuser;

### 1.2 Code download
- Download from git **[repository](https://github.com/Surtrade/surtrade_api)**
- if you have a branch type: git remote add origin  <REMOTE_URL> 

### 1.3 Create virtual environment
- Tutorial to create a **[Virtualenv](https://virtualenv.pypa.io/en/stable/)**
- If .env already exists, update information in the file
- To activate environment type in terminal "source .env"

### 1.4 Install Requirements
- To install requirements type: pip install -r requirements.txt
- To create requirements.txt type "pip freeze > requirements.txt"

### 1.5 SQLAlchemy Setup
- To generate database type "python manage.py db init"
- To migrate the data type "python manage.py db migrate"
- To apply the data type "python manage.py db upgrade"

## 2 Run
### 2.a Local Server
- To start server type "flask run"

### 2.b Linux
#### 2.b.1 Gunicorn
Tutorial to setup Flask with Gunicorn:**[Get Started](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04)**
- To open the 5000 port type "sudo ufw allow 5000"
- To run server type "python run.py"
- To set it up type "gunicorn --bind 0.0.0.0:5000 wsgi:app"
#### 2.b.2Processes in Gunicorn
- To see the processes: ps ax|grep gunicorn and to stop gunicorn_django is pkill gunicorn

### 2.c Local Tunnel
- To open a tunnel type: lt --port 5000 --subdomain surtrade




