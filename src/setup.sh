#!/bin/bash
sudo apt-get update
sudo apt-get install python-pip python-dev mysql-server libmysqlclient-dev
sudo mysql_install_db
mysql -u root -p << EOM
CREATE DATABASE equipotest CHARACTER SET UTF8;
CREATE USER test_user@localhost IDENTIFIED BY 'test_user_pwd';
GRANT ALL PRIVILEGES ON equipotest.* TO test_user@localhost;
FLUSH PRIVILEGES;
EOM
sudo pip install django mysqlclient
./manage.py makemigrations
./manage.py migrate
sudo pip install djangorestframework
sudo pip install django-extensions

