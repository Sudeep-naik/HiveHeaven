create database HiveHaven;
-- Create Users table
use HiveHaven;
-- Table: apartment
CREATE TABLE IF NOT EXISTS apartments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    appartment_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100)
);

-- Table: user
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    phone_no varchar(40),
	apartment_id INT,
    house_no int,
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES apartments(id)
);

-- Table: department
CREATE TABLE IF NOT EXISTS departments (
    apartment_id INT,
    dep_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES apartments(id)
);
-- drop table department;

-- Table: complaint
CREATE TABLE IF NOT EXISTS department_complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    department_id INT,
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status int DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (department_id) REFERENCES departments(dep_id)
);
-- drop table department_complaint;

CREATE TABLE IF NOT EXISTS neighbor_complaints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    neighbor_user_id INT,
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status int DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (neighbor_user_id) REFERENCES users(user_id)
);
-- drop table neighbor_complaint;
