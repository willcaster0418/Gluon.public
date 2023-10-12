DROP USER IF EXISTS 'oms'@'localhost';
CREATE USER 'oms'@'localhost';
GRANT ALL PRIVILEGES ON *.* TO 'oms'@'localhost' WITH GRANT OPTION;