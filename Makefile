silent:

up:
	flask run -p 8000

db_init:
	flask db init

migrate:
	flask db migrate

upgrade:
	flask db upgrade

