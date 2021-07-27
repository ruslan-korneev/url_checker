#!/bin/bash

# Create Environment "Virtual Environment file path", "Deploy Flag file path"
VENV=./venv
DEPLOY_FLAG=/opt/url_checker/deploy_state.flag

# Create flag file in current dir
touch $DEPLOY_FLAG

# Check if not exists VENV, -> create VENV
if [ ! -d $VENV ]; then
    `which python3` -m venv $VENV
    $VENV/bin/pip install -U pip
fi
`which python3` -m venv $VENV
# Upgrade pip
$VENV/bin/pip install -U pip
# Installing requirements from file
$VENV/bin/pip install -r requirements.txt

# Do migrate (for creating tables in the database) 
$VENV/bin/python src/manage.py migrate
$VENV/bin/python src/manage.py collectstatic --no-input

cd src

echo "Run Celery Beat"
../$VENV/bin/celery -A url_checker beat --detach -l INFO -f ../logs/beat.log

echo "Run Celery Worker"
../$VENV/bin/celery -A url_checker worker --detach -l INFO --pool=solo -f ../logs/worker.log

echo "Run Django"
../$VENV/bin/python manage.py runserver 0.0.0.0:8000

# When app will be stoped, remove Deploy Flag
rm -f ../$DEPLOY_FLAG
