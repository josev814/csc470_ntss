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
docker compose -f "Build/docker-compose.yml" down --volumes --remove-orphans
```
- (--volumes|-v)
  - Removes named and anonymous volumes pertaining to the service
- --rmi (local|all)
  - Removes the images used for the application


# Project Development
This project uses the MVC convention

## Routes
In **wsgi.py**, add any routes that should be detected by our application.
You will use `@application` which is an instance of the Routes class.
Then you will call the route method.  The route method takes the path as the first argument.
The second argument is a list of the methods that the route supports such as GET, POST, PATCH, UPDATE, DELETE.
```python
@application.route('/dashboard', methods=['GET'])
```

After defining the route, create a function that will take in the the request and response as the first two parameters.
Within the function, you call the other classes that the function should call.
The example below will load the dashboard page.

```python
@application.route('/dashboard', methods=['GET'])
def dashboard(request, response):
    output = NtssController().dashboard()
    response.status_code = 200
    response.text = output
    return [output]
```

##

[Project.md]: ./Project.md
