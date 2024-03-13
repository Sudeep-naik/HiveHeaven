create database HiveHaven;
-- Create Users table
use HiveHaven;
-- Table: apartment
CREATE TABLE IF NOT EXISTS Apartment (
    apartment_id varchar(100) PRIMARY KEY,
    apartment_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100)
);
-- drop table apartments;

-- Table: user
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    phone_no varchar(40),
	apartment_id varchar(100),
    house_no int,
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES Apartment(apartment_id)
);
-- drop table users;
-- Table: department
CREATE TABLE IF NOT EXISTS Department (
    apartment_id varchar(100),
    dep_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES Apartment(apartment_id)
);
-- drop table department;

-- Table: complaint
CREATE TABLE IF NOT EXISTS DepartmentComplaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    department_id INT,
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status int DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (department_id) REFERENCES Department(dep_id)
);
-- drop table department_complaint;

CREATE TABLE IF NOT EXISTS NeighborComplaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    neighbor_user_id INT,
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status int DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (neighbor_user_id) REFERENCES Users(user_id)
);
--  drop table neighbor_complaint;

INSERT INTO apartment (apartment_id, apartment_name, address, city, state) VALUES
('APT001', 'Royal Residency', '34 Park Street', 'Kolkata', 'West Bengal'),
('APT002', 'Green Valley Apartments', '21 Gandhi Nagar', 'Bangalore', 'Karnataka'),
('APT003', 'Riverside Towers', '56 M.G. Road', 'Mumbai', 'Maharashtra'),
('APT004', 'Sunset Heights', '89 Rajaji Nagar', 'Chennai', 'Tamil Nadu');


select * from apartments;