#!/bin/sh
set -e
cp -n .env.example .env

docker compose build
docker compose up --no-start
