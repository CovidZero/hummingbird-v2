# hummingbird-v2


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
export FLASK_APP=src/main.py
export FLASK_ENV=development
```


## Running local
___
```
export FLASK_ENV=development

flask run
or
python src/main.py 
```

## Setup database
___

- Local
```
export FLASK_ENV=development
flask db init --directory=local_migrations
flask db migrate --directory=local_migrations
flask db upgrade --directory=local_migrations   
```

