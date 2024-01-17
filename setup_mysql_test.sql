-- Preparing MySQL Server for the Project.                                                                         
-- Creating the `hbnb_test_db` database.
-- Creating the `hbnb_test` user at `localhost` with a password.
-- Granting ALL priviliges on the `hbnb_test_db` and SELECT priviliges
-- on the `performance_schema`.
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
