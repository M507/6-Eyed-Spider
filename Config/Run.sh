#!/bin/bash

# Start the database
docker-compose -f docker-compose-db.yml up --build -d
# Wait 
sleep 25
# Load the premade database
docker exec -i strapi-docker_db_1 sh -c 'mongorestore --archive=/data/db.dump'

# Start web and strapi 
docker-compose -f docker-compose-main.yml up --build -d

# list them
docker ps
