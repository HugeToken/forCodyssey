CREATE DATABASE IF NOT EXISTS mars_db;
USE mars_db;
CREATE TABLE mars_weather (
    weather_id INT AUTO_INCREMENT PRIMARY KEY,
    mars_date DATETIME NOT NULL,
    temp INT,
    storm INT
);