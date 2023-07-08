CREATE USER 'kea'@'%' IDENTIFIED WITH mysql_native_password BY 'secret123';
GRANT ALL PRIVILEGES ON kea.* TO 'kea'@'%' WITH GRANT OPTION;