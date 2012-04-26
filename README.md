[![Flattr this repo!](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=mattoufoutu&url=https://github.com/mattoufoutu/shorty&title=shorty&language=&tags=github&category=software)

## Introduction

Shorty is an URL shortener written in Python using the Flask framework.

## Dependencies

- Flask==0.8
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Script (only needed to run the application from the `manage.py` script)

## Running it

Install the required dependencies with `pip`

    pip install -r requirements.txt

Set up the database

    python manage.py syncdb

and then, to run it with the Flask's development server, use the `manage.py` script

    python manage.py runserver

To run the application in a production environment, refer to [Flask's documentation]
(http://flask.pocoo.org/docs/deploying/)
about deployment options.
