# Hummingbird V2
![Python Tests](https://github.com/CovidZero/hummingbird-v2/workflows/Python%20Tests/badge.svg)
![Python Code Style Enforcement](https://github.com/CovidZero/hummingbird-v2/workflows/Python%20Code%20Style%20Enforcement/badge.svg)
![Auto Assign](https://github.com/CovidZero/hummingbird-v2/workflows/Auto%20Assign/badge.svg)


## Project Resources
___
- Language: Python 3.7
- Package manager: pip
- Main dependencies: Flask 1.1.1, Flask-RESTPus
- Tests: unittests


## Setup dependencies
___
```
cd hummingbird-v2
virtualenv venv
source venv/bin/activate
pip install -r src/requirements.txt
pip install -r requirements_local.txt
```

## Variables setup
___
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export FLASK_ENV=development
```


## Running local machine
___
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export FLASK_ENV=development
python src/main.py 
```

## Running with docker-compose

___
```
docker-compose up --build

```

## Swagger API Doc 
http://127.0.0.1:5000/data_api/v1/


## To Setup database locally
___

- Local
```
export FLASK_APP=src/main.py
export FLASK_ENV=development
flask db init --directory=local_migrations
flask db migrate --directory=../local_migrations
flask db upgrade --directory=local_migrations   
```


## To run tests locally
___
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export FLASK_ENV=testing
python tests/runner.py
```

## To run Flake 8 For Style Guide Enforcement
___
```
flake8 src
```


## Setup Docker

#### Start your environment using docker
___
```
docker-compose up
```

#### Configure database to develop

___
```
$ docker exec -it api /bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/src
export FLASK_APP=src/main.py
export FLASK_ENV=development
flask db init --directory=local_migrations
flask db migrate --directory=../local_migrations
flask db upgrade --directory=local_migrations  

```
