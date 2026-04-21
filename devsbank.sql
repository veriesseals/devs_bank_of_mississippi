-- In MySQL, make a database (names can match your .env):

CREATE DATABASE devsbank CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'root'@'%' IDENTIFIED BY 'Tyaanah201!';
GRANT ALL PRIVILEGES ON devsbank.* TO 'root'@'%';
FLUSH PRIVILEGES;
