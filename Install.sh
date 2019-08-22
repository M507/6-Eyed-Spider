#!/bin/bash
rm -rf strapi-docker
git clone https://github.com/strapi/strapi-docker && cd strapi-docker
rm docker-compose.yml
cp ../Config/docker-compose-db.yml ../Config/docker-compose-main.yml ../Config/Run.sh .
# cp ../server.json ./strapi-app/config/environments/development/server.json
mkdir database
cp ../Database/db-RedAdmin.dump ./database/db.dump
