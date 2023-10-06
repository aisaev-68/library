#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py test tests.test_all
python manage.py create_groups
python manage.py create_authors_books
#python manage.py dumpdata category > tests/fixtures/all_db-fixtures.json
python manage.py runserver 0.0.0.0:8000