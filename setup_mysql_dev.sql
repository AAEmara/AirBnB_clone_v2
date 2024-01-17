-- Preparing MySQL Server for the Project.                                                                         
-- Creating the `hbnb_dev_db` database.
-- Creating the `hbnb_dev` user at `localhost` with a password.
-- Granting ALL priviliges on the `hbnb_dev_db` and SELECT priviliges
-- on the `performance_schema`.
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
