#!/bin/bash

docker-compose -f devops/localhost/docker-compose.yml down || true
docker-compose -f devops/localhost/docker-compose.yml up
