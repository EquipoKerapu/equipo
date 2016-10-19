#!/bin/bash
mysql -u root -p << EOM
CREATE DATABASE equipotest CHARACTER SET UTF8;
CREATE USER test_user@localhost IDENTIFIED BY 'test_user_pwd';
GRANT ALL PRIVILEGES ON equipotest.* TO test_user@localhost;
FLUSH PRIVILEGES;
EOM

