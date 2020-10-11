# Example Headless lieblingsladen.gera.de

## General Information

- Original Repo: https://github.com/mirumee/saleor-platform
- This Project is a rudimentary

## Background

The site [lieblingsladen.gera](https://lieblingsladen.gera.de/) is to be converted into a regional marketplace for the city of Gera. This project shall help to visualize a headless e-commerce approach.

## Requirements

general:

- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

for example populate:

- python3
- modules: aiogqlc, requests

for remote setup on ubuntu:

- local machine is linux distro
- python3
- modules: ansible

All python modules are included in `/setup/pipfile` for a virtual env.

## Setup python virualenv:

1. install [pipenv](https://pypi.org/project/pipenv/)
2. navigate into `/setup`
3. run `pipenv install`
4. run `pipenv shell`

### Local setup

1. cd into repo.
2. Follow [official dokumentation](https://docs.saleor.io/docs/developer/installation/). Instead of using the default `docker-compose.yml` use d`ocker-compose.customfrontend.yml`.

Example:
`docker-compuse -f docker-compose.customfrontend.yml up`

### Remote Ubuntu setup

Required:

- basic Ansible knowledge

Steps:

1. add `hosts` file to `ansible/config/`
2. add your host to it (see [Ansible Documentation](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html))
3. navigate to `/setup/` and run `source export_env.sh`
4. add private key fore server to ssh agend
5. navigate to `ansible`
6. update `access_control_allow_origin` in `setup_server.yml` to match your domain
7. run `ansible-playbook setup_server.yml`
8. do setp 2 of local setup on remote system

Docker-compose file: `docker-compose.customfrontend.cloud.yml`

## How to run it?

See [Original Doku](https://github.com/mirumee/saleor-platform).

Difference:

- Run `docker-compose.customfrontend.yml` instad of `docker-compose.yml` with docker compose. (like in local setup)

### Example Populate

1. edit `GRAPHQL_URL` to match your env.
2. export env. var `GRAPHQL_BEAR_TOKEN` with your bear token ([How to create token with api?](https://docs.saleor.io/docs/developer/extending/apps)/ [Dashboard](https://docs.saleor.io/docs/dashboard/configuration/service-accounts))

## Where is the application running locally?

- Gera Storefront - http://localhost:3000
- Saleor Dashboard - http://localhost:9000
- Saleor Core (API) - http://localhost:8000
- Jaeger UI (APM) - http://localhost:16686
- Mailhog (Test email interface) - http://localhost:8025

## Licence

See [BSD 3-Clause License](LICENSE.md).
