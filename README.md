sudo apt install -y mysql-server python3.10-dev pkg-config build-essential
sudo apt install -y libmysqlclient-dev default-libmysqlclient-dev
CREATE USER 'degen'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON _._ TO 'sammy'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;
