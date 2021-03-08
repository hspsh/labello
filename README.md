# Labello

Aim of this project is to create label library and control software for zebra printer and other alike.

## Development

```bash
# we are using poetry for dependency management
poetry install
poetry shell

# run once to create database
PYTHONPATH=. python helpers/db_create.py

# run app in for developement in virtual env
FLASK_APP=labello.web FLASK_ENV=development flask run
# or
poetry run python -m labello
```
