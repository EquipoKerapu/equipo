#!/bin/bash
sudo pip install django mysqlclient
sudo pip install djangorestframework
sudo pip install django-extensions
./manage.py makemigrations
./manage.py migrate