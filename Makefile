.ONESHELL:

.PHONY : all exec clean info

override container_id := $(shell docker ps | grep django | head -c 12)

all: 
	@docker-compose -f ./docker-compose.yml build
	docker-compose -f ./docker-compose.yml up -d
	sleep 2
	docker-compose exec django python manage.py migrate

exec:
ifeq ($(strip $(container_id)),)
	@echo "No Django container was found" && exit 1
else
	@docker exec -it $(container_id) /bin/bash 2>/dev/null
endif

clean:
	@if [ -z "$$(docker ps -q)" ] && [ -z "$$(docker ps -aq)" ] && [ -z "$$(docker images -q)" ]; then \
	echo "${green}Already clean${reset}"; fi
	if [ ! -z "$$(docker ps -q)" ]; then docker stop $$(docker ps -q); fi
	if [ ! -z "$$(docker ps -aq)" ]; then docker rm $$(docker ps -aq); fi
	if [ ! -z "$$(docker images -q)" ]; then docker rmi $$(docker images -q); fi

info:
	@echo "${green}I M A G E S ${reset}" 
	docker images
	echo "${green}C O N T A I N E R S ${reset}"
	docker ps -a


# V A R I A B L E S
green=\033[32m
reset=\033[0m