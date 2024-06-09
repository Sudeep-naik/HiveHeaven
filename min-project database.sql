create database web_project;
-- drop database web_project;
use web_project;
CREATE TABLE Apartment (
    apartment_id VARCHAR(100) PRIMARY KEY,
    apartment_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100)
);

CREATE TABLE Users (
    user_id VARCHAR(100) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    phone_no VARCHAR(40),
    apartment_id VARCHAR(100),
    house_no INT,
    email VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES Apartment(apartment_id)
);

CREATE TABLE Admin (
    admin_id VARCHAR(100) PRIMARY KEY,
    admin_name VARCHAR(100) NOT NULL,
    apartment_id VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    admin_password VARCHAR(255) NOT NULL,
    FOREIGN KEY (apartment_id) REFERENCES Apartment(apartment_id)
);

CREATE TABLE Department (
    apartment_id VARCHAR(100),
    dep_id INT AUTO_INCREMENT,
    department_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (dep_id),
    FOREIGN KEY (apartment_id) REFERENCES Apartment(apartment_id)
);

CREATE TABLE DepartmentComplaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100),
    department_id INT,
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (department_id) REFERENCES Department(dep_id)
);

CREATE TABLE NeighborComplaint (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(100),
    neighbor_user_id VARCHAR(100),
    subject VARCHAR(255) NOT NULL,
    description VARCHAR(800),
    status INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (neighbor_user_id) REFERENCES Users(user_id)
);

INSERT INTO Apartment (apartment_id, apartment_name, address, city, state) 
VALUES 
('APT0001', 'Sunnydale Apartments', '456 Oak Avenue', 'Mumbai', 'Maharashtra'),
('APT0002', 'Riverview Condos', '789 Pine Road', 'Bengaluru', 'Karnataka'),
('APT0003', 'Mountain View Apartments', '1010 Elm Street', 'Shimla', 'Himachal Pradesh'),
('APT0004', 'Lakeside Apartments', '2020 Lake Drive', 'Udaipur', 'Rajasthan'),
('APT0005', 'City Center Apartments', '3030 Main Street', 'Hyderabad', 'Telangana'),
('APT0006', 'Beachside Apartments', '4040 Ocean Blvd', 'Chennai', 'Tamil Nadu'),
('APT0007', 'Forest Heights Apartments', '5050 Forest Lane', 'Dehradun', 'Uttarakhand'),
('APT0008', 'Parkside Residences', '6060 Park Ave', 'Gurgaon', 'Haryana'),
('APT0009', 'Sunset Villas', '7070 Sunset Blvd', 'Goa', 'Goa');

INSERT INTO Department (apartment_id, department_name, email) VALUES
('APT0001', 'Maintenance', 'maintenance@example.com'),
('APT0001', 'Plumbing', 'plumbing@example.com'),
('APT0001', 'Electrical', 'electrical@example.com');


select *from users;
delete from users where user_id="APT0001-103";
select * from Admin;