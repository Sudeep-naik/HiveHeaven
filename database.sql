create database web_project;
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
    PRIMARY KEY (apartment_id, dep_id),
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
