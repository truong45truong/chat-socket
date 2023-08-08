compose:
	sudo docker compose build
	sudo docker compose up
compose-up:
	sudo docker compose up
run-redis:
	sudo docker run --rm -p 6379:6379 redis:5
compose-build:
	sudo docker compose build
makemigrations:
	make backend-terminal cmd="python3 manage.py makemigrations"
migrate:
	make backend-terminal cmd="python3 manage.py migrate"
create-admin:
	make backend-terminal cmd="python3 manage.py createsuperuser"
createdb:
	sudo docker exec -it postgres createdb --username=user --owner=user simple_chat
dropdb:
	sudo docker exec -it postgres dropdb --username=user simple_chat
check-port:
	sudo lsof -i :5050
	sudo lsof -i :5432
kill-port:
	sudo kill $(PID)
start-app:
	python3 ./backend/manage.py startapp  $(name)
backend-terminal:
	sudo docker exec -it socketchat-backend-1 $(cmd)
postgres:
	sudo docker exec -it postgres psql -U User  simple_chat
.PHONY: compose createdb dropdb postgres compose-up compose-build startapp backend-terminal create-admin makemigrations run-redis