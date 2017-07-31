#!/bin/bash
cd /home/adfs/postgresql/
    docker-compose stop
    docker-compose rm

    docker rmi postgres

    docker-compose up -d
