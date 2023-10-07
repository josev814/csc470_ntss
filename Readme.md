# Project description
This is part of Fayetteville State University's CSC470 class

The project description can be found in [Project.md]

# Requirements
Python

Docker
- MariaDB (mysql database)

# The Docker application
We use docker compose to build app image and to link the app to mariadb.

## Configuration
Under the Build directory copy the dbenvvars.example and name it .dbenvvars
Edit the .dbenvvars to have the database creds you want for the db

Do the same for the appenvvars.example file.

## Standing up the application
```bash
docker compose -f Build/docker-compose.yml up -d --build --remove-orphans
```

or

```bash
docker-compose -f Build/docker-compose.yml build --no-cache && docker compose -f Build/docker-compose.yml up -d
```
### The used flags
- -f
  - Defines where the compose file is
- --build
  - Builds images before starting containers
- --remove-orphans
  - Removes containers for services not listed in the compose file for the project

### additional build options for docker
- --force-create
  - this allows us to force recreating of the images
- --no-cache
  - do not use any cache when building the images
- --always-recreate-deps
  - this allows to recreate the dependent containers


## Teardown the application
```bash
docker compose -f "Build/docker-compose.yml" down --volumes
```
- (--volumes|-v)
  - Removes named and anonymous volumes pertaining to the service
- --rmi (local|all)
  - Removes the images used for the application




[Project.md]: ./Project.md