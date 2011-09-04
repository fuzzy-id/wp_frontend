CREATE USER 'test_user'@'localhost' IDENTIFIED BY 'D3v3L0p3R';
CREATE DATABASE IF NOT EXISTS testing;
GRANT ALL ON testing.* TO 'test_user'@'localhost';
