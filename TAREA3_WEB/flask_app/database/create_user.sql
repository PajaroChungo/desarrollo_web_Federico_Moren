-- Active: 1778285556064@@127.0.0.1@3306@tarea2
--Crear Usuario
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
--Eliminar usuario de ser necesario
DROP USER 'dbadmin'@'localhost';