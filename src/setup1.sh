#!/bin/bash
sudo apt-get update
sudo apt-get --assume-yes install python-pip python-dev mysql-server libmysqlclient-dev
sudo mysql_install_db
