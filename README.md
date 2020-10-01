# saleor-platform
All Saleor services started from a single repository

*Keep in mind this repository is for local development only and is not meant to be deployed on any production environment! If you're not a developer and just want to try out Saleor you can check our [live demo](https://demo.saleor.io/).*

## Requirements
1. [Docker](https://docs.docker.com/install/)
2. [Docker Compose](https://docs.docker.com/compose/install/)


## How to run it?

Build the application:
```
docker-compose build
```
OR
```
docker-compose -f docker-compose.customfrontend.yaml build
```

Apply Django migrations:
```
docker-compose run --rm api python3 manage.py migrate
```

Collect static files:
```
docker-compose run --rm api python3 manage.py collectstatic --noinput
```

Populate the database with example data and create the admin user:
```
docker-compose run --rm api python3 manage.py populatedb --createsuperuser
```

Run the application:
```
docker-compose up
```
OR
```
docker-compose -f docker-compose.customfrontend.yaml up
```
*Both storefront and dashboard are quite big frontend projects and it might take up to few minutes for them to compile depending on your CPU. If nothing shows up on port 3000 or 9000 wait until `Compiled successfully` shows in the console output.*

You can find the latest version of Saleor, storefront and dashboard in their individual repositories:

- https://github.com/mirumee/saleor
- https://github.com/mirumee/saleor-dashboard
- https://github.com/mirumee/saleor-storefront

## How to solve issues with lack of available space or build errors after update

Most of the time both issues can be solved by cleaning up space taken by old containers. After that, we build again whole platform. 


1. Make sure docker stack is not running
```
$ docker-compose stop
```

2. Remove existing volumes

**Warning!** Proceeding will remove also your database container! If you need existing data, please remove only services which cause problems! https://docs.docker.com/compose/reference/rm/
```
docker-compose rm
```

3. Build fresh containers 
```
docker-compose build
```

4. Now you can run fresh environment using commands from `How to run it?` section. Done!

### Still no available space

If you are getting issues with lack of available space, consider prunning your docker cache:

**Warning!** This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - all dangling build cache 
  
  More info: https://docs.docker.com/engine/reference/commandline/system_prune/
  
<details><summary>I've been warned</summary>
<p>

```
$ docker system prune
```

</p>
</details>

## How to run application parts?
  - `docker-compose up api worker` for backend services only
  - `docker-compose up` for backend and frontend services


## Where is the application running?
- Saleor Core (API) - http://localhost:8000
- Saleor Storefront - http://localhost:3000
- Saleor Dashboard - http://localhost:9000
- Jaeger UI (APM) - http://localhost:16686
- Mailhog (Test email interface) - http://localhost:8025 

