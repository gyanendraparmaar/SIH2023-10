CREATE DATABASE newsDatabase CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE newsDatabase;
CREATE TABLE articles (
                          id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                          link VARCHAR(100) NOT NULL,
                          title VARCHAR(100) NOT NULL,
                          content TEXT NOT NULL,
                          created DATETIME NOT NULL,
                          sentiment FLOAT(3,2) NOT NULL,
                          department VARCHAR(100) NOT NULL
);
CREATE TABLE users (
                       id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
                       department VARCHAR(255) NOT NULL,
                       hashed_password CHAR(60) NOT NULL,
                       created DATETIME NOT NULL,
                       writeAcess BOOLEAN NOT NULL DEFAULT TRUE
);
