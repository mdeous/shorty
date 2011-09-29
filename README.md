## Introduction

Shorty is an URL shortener written in Python using the Flask framework.

## Dependencies

- Flask
- Flask-WTF
- Flask-Script (only needed to run the application from the `manage.py` script)

## Running it

Install the required dependencies with `pip`

    pip install -r dependencies.txt

and then, to run it with the Flask's development server, use the `manage.py` script

    python manage.py runserver

To run the application in a production environment, refer to [Flask's documentation]
(http://flask.pocoo.org/docs/deploying/)
about deployment options.
