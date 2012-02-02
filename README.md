## Introduction

Shorty is an URL shortener written in Python using the Flask framework.

## License

Shorty's source code is licensed under the [GNU General Public License]
(https://www.gnu.org/licenses/gpl.txt).

## Dependencies

- Flask==0.8
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Login
- Flask-Script (only needed to run the application from the `manage.py` script)

## Running it

Install the required dependencies with `pip`

    pip install -r requirements.txt

Set up the database using the `manage.py` script

    python manage.py syncdb

and then, to run it with the Flask's development server, use the `runserver` command

    python manage.py runserver

To run the application in a production environment, refer to [Flask's documentation]
(http://flask.pocoo.org/docs/deploying/)
about deployment options.
