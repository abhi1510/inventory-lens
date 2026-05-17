#!/bin/bash

docker-compose down -v
docker rmi inventory-lens-app
docker rmi inventory-lens-notification
docker-compose build --no-cache
docker-compose up -d
