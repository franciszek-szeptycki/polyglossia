#!/bin/bash

docker-compose -f devops/localhost/docker-compose.yml exec -ti database psql -U polyglossia
