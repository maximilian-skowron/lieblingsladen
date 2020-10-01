# Example Headless lieblingsladen.gera.de

## General Information

- Original Repo: https://github.com/mirumee/saleor-platform
- This Project is a rudimentary proof of concept

## Background

The site [lieblingsladen.gera](https://lieblingsladen.gera.de/) is to be converted into a regional marketplace for the city of Gera. This project shall show how such a market place could look like by using a headless ecomerce approach.

## Requirements

1. [Docker](https://docs.docker.com/install/)
2. [Docker Compose](https://docs.docker.com/compose/install/)

## Fast Ansible Server Setup (for Ubuntu)

- Required: Ansible Knowledge
- TODO: Change hosts in ansible/setup_server.yml
- Run: `ansible-playbook setup_server.yml`

## How to run it?

See [Original Doku](https://github.com/mirumee/saleor-platform).

Difference:

- Run docker-compose.customfrontend.yml instad of docker-compose.yml with docker compose.
- folder name is lieblingsladen

## Where is the application running?

- Gera Storefront - http://localhost:3000
- Saleor Dashboard - http://localhost:9000
- Saleor Core (API) - http://localhost:8000
- Jaeger UI (APM) - http://localhost:16686
- Mailhog (Test email interface) - http://localhost:8025
