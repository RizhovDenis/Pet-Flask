# Descripsion
### Set dependencies
~~~
pip3 install -r requirements.txt
~~~
### Create Database
~~~
sudo su - postgres
~~~
~~~
psql
~~~
~~~
CREATE DATABASE humanity;
~~~
### Open database
~~~
psql -U postgres -d humanity -h localhost -W
~~~
### Alembic instructions
~~~
alembic init migrations
~~~
Generate migration after adding or deliting 
~~~
alembic revision -m "init" --autogenerate
~~~
~~~
alembic upgrade head
~~~
### Create fixtures
~~~
python3 fixtures.py
~~~
### Launch app
~~~
python3 run_server.py
celery -A run_celery worker --loglevel INFO
~~~
