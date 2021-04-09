PROJECTNAME=$(shell basename "$(PWD)")
.DEFAULT_GOAL := help
.EXPORT_ALL_VARIABLES:
PROJECT ?= ''

## make help: command for show itself help info
help: Makefile
	@echo " Choose a command run in "$(PROJECTNAME)":"
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'

## make build: command to build service
build:
	@docker-compose -p ${PROJECT} build

## make up: command to start demo
up:
	@docker-compose -p ${PROJECT} up -d db
	@docker-compose -p ${PROJECT} up -d redis
	@sleep 10
	@docker-compose -p ${PROJECT} up -d app


## make down: command to stop demo
down:
	@docker-compose -p ${PROJECT} down
