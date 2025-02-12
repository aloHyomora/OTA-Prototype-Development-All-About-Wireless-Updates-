#create database db_name;
SHOW DATABASES;
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'Flask@1234'; # 비밀번호 다름
GRANT ALL PRIVILEGES ON *.* TO 'flaskuser'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
