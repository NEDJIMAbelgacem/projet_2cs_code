CREATE USER 'user'@'localhost' IDENTIFIED BY '1475369';
create database station_db;
GRANT ALL PRIVILEGES ON station_db.* TO 'database_user'@'localhost';

CREATE TABLE IF NOT EXISTS vehicles(name VARCHAR(32), matricule VARCHAR(32), id INT NOT NULL AUTO_INCREMENT PRIMARY KEY);

CREATE TABLE IF NOT EXISTS missions(start DATETIME, end DATETIME, vehicule_id INT, id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    FOREIGN KEY(vehicule_id) REFERENCES vehicles(id));

CREATE TABLE IF NOT EXISTS data_records(record_time DATETIME, vehicule_id INT, mission_id INT, id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY(vehicule_id) REFERENCES vehicles(id)),
    FOREIGN KEY(mission_id) REFERENCES missions(id))
    );

CREATE TABLE IF NOT EXISTS variables(record_id INT, pid_code VARCHAR(30), description VARCHAR(200), value VARCHAR(100), id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY(record_id) REFERENCES data_records(id))
    );
