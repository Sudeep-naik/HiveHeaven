create database HiveHaven;
-- Create Users table
drop database HiveHaven;
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
    user_id varchar(100) PRIMARY KEY,
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
truncate Department;
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
    FOREIGN KEY (department_id) REFERENCES Department(dep_id),
    primary key(id,user_id)
);
drop table department_complaint;

CREATE TABLE IF NOT EXISTS NeighborComplaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    neighbor_user_id INT,
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status int DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
drop table neighborcomplaint;

INSERT INTO apartment (apartment_id, apartment_name, address, city, state) VALUES
('APT001', 'Royal Residency', '34 Park Street', 'Kolkata', 'West Bengal'),
('APT002', 'Green Valley Apartments', '21 Gandhi Nagar', 'Bangalore', 'Karnataka'),
('APT003', 'Riverside Towers', '56 M.G. Road', 'Mumbai', 'Maharashtra'),
('APT004', 'Sunset Heights', '89 Rajaji Nagar', 'Chennai', 'Tamil Nadu');

INSERT INTO Department (apartment_id, department_name, email) VALUES 
('APT002',  'Electrician', 'electrician@example.com'),
('APT002',  'Plumbing', 'plumbing@example.com'),
('APT002',  'HVAC', 'hvac@example.com'),
('APT002',  'Maintenance', 'maintenance@example.com'),
('APT002',  'Carpentry', 'carpentry@example.com'),
('APT002',  'Janitorial', 'janitorial@example.com'),
('APT002',  'IT Support', 'itsupport@example.com'),
('APT002',  'Security', 'security@example.com'),
('APT002',  'Cleaning', 'cleaning@example.com');

INSERT INTO NeighborComplaint (user_id, neighbor_user_id, subject, description, status)
VALUES
    (11, 12, 'Excessive Noise', 'My neighbor plays loud music late at night.', 0),
    (11, 12, 'Parking Issue', 'My neighbor keeps parking in my designated spot.', 0),
    (12, 11, 'Trash Disposal Problem', 'My neighbor often leaves trash outside our door.', 0);
INSERT INTO DepartmentComplaint (user_id, department_id, subject, description, status, created_at)
VALUES
    (11, 10, 'Network Issues', 'Experiencing network connectivity problems', 0, NOW()),
    (11, 11, 'Printer Malfunction', 'Printer in the department is not working', 0, NOW()),
    (11, 12, 'Software Installation', 'Need assistance with software installation', 0, NOW());

delete from Users where apartment_id="APT002";
select *from Users;
select *from Department;
select * from Apartment;
select * from NeighborComplaint;
truncate NeighborComplaint;