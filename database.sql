create database web_project;
-- drop database web_project;
use web_project;
CREATE TABLE users (
    user_id CHAR(36) NOT NULL PRIMARY KEY,
    user_name VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    phone_no VARCHAR(14),
    address VARCHAR(60),
    userpass VARCHAR(255) NOT NULL
);

CREATE TABLE vehicle (
    vehicle_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    vehicle_name VARCHAR(50),
    make VARCHAR(60),
    model VARCHAR(60),
    make_year INT,
    licence_number VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE registration_documents (
    registration_id CHAR(36) NOT NULL PRIMARY KEY,
    vehicle_id INT NOT NULL,
    document_name VARCHAR(50) NOT NULL,
    document_number VARCHAR(20) UNIQUE,
    expiration_date DATE,
    file_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE insurance_documents (
    insurance_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    policy_number VARCHAR(40),
    expire_date DATE,
    file_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE emissiondocuments (
    emission_id CHAR(36) NOT NULL PRIMARY KEY,
    vehicle_id INT NOT NULL,
    certificate_number VARCHAR(30),
    issue_date DATE,
    expiration_date DATE,
    file_path VARCHAR(255) NOT NULL,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle(vehicle_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
-- Users
INSERT INTO users (user_id, user_name, email, phone_no, address, userpass) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'John Doe', 'john.doe@example.com', '555-1234', '123 Elm St', 'password123'),
('550e8400-e29b-41d4-a716-446655440001', 'Jane Smith', 'jane.smith@example.com', '555-5678', '456 Oak St', 'securepass'),
('550e8400-e29b-41d4-a716-446655440002', 'Alice Johnson', 'alice.johnson@example.com', '555-8765', '789 Pine St', 'mypassword');

-- Vehicles
INSERT INTO vehicle (user_id, vehicle_name, make, model, make_year, licence_number) VALUES
('550e8400-e29b-41d4-a716-446655440000', 'John\'s Car', 'Toyota', 'Corolla', 2015, 'ABC123'),
('550e8400-e29b-41d4-a716-446655440001', 'Jane\'s SUV', 'Honda', 'CR-V', 2018, 'XYZ789'),
('550e8400-e29b-41d4-a716-446655440002', 'Alice\'s Truck', 'Ford', 'F-150', 2020, 'LMN456');

-- Registration Documents
INSERT INTO registration_documents (registration_id, vehicle_id, document_name, document_number, expiration_date, file_path) VALUES
('a5d5c5b1-9b34-4e5c-b4af-123456789abc', 1, 'Registration', 'REG123', '2024-12-31', '/documents/reg123.pdf'),
('b7d7c7e3-8d56-4f7d-b8ce-234567890bcd', 2, 'Registration', 'REG456', '2025-06-30', '/documents/reg456.pdf'),
('c9d9e9f5-0e78-4f9f-c0de-345678901cde', 3, 'Registration', 'REG789', '2026-03-31', '/documents/reg789.pdf');

-- Insurance Documents
INSERT INTO insurance_documents (vehicle_id, policy_number, expire_date, file_path) VALUES
(1, 'POL123', '2024-11-30', '/documents/ins123.pdf'),
(2, 'POL456', '2025-05-31', '/documents/ins456.pdf'),
(3, 'POL789', '2026-02-28', '/documents/ins789.pdf');

-- Emission Documents
INSERT INTO emissiondocuments (emission_id, vehicle_id, certificate_number, issue_date, expiration_date, file_path) VALUES
('d7e7f7g9-1f23-4a5c-b5de-456789012def', 1, 'EM123', '2023-12-01', '2024-12-01', '/documents/em123.pdf'),
('e8f8g8h1-2g34-4b5d-c6ef-567890123fgh', 2, 'EM456', '2024-01-15', '2025-01-15', '/documents/em456.pdf'),
('f9g9h9i3-3h45-4c6e-d7fg-678901234ghi', 3, 'EM789', '2024-03-20', '2025-03-20', '/documents/em789.pdf');


SELECT u.user_name, u.email, v.vehicle_name, v.make, v.model, v.licence_number
FROM users u
JOIN vehicle v ON u.user_id = v.user_id;


SELECT v.vehicle_name, v.licence_number, i.policy_number, i.expire_date
FROM vehicle v
JOIN insurance_documents i ON v.vehicle_id = i.vehicle_id
WHERE i.expire_date < DATE_ADD(CURDATE(), INTERVAL 3 MONTH);

SELECT rd.document_name, rd.document_number, rd.expiration_date, v.vehicle_name, v.licence_number, u.user_name, u.email
FROM registration_documents rd
JOIN vehicle v ON rd.vehicle_id = v.vehicle_id
JOIN users u ON v.user_id = u.user_id;

SELECT u.user_name, u.email, v.vehicle_name, v.make, v.model, v.make_year
FROM users u
JOIN vehicle v ON u.user_id = v.user_id
WHERE v.make_year > 2018;


select * from vehicle where user_id="f8d7df56-23a2-466a-93dc-996c67d9e225";
select * from vehicle where make_year=2020 ;
select * from registration_documents;
select *from insurance_documents where expire_date>"2022-02-11";
select * from registration_documents where vehicle_id="1";

select * from vehicle;
select * from vehicle where user_id="f8d7df56-23a2-466a-93dc-996c67d9e225";
-- truncate users;
-- truncate vehicle;
-- select *from vehicle;
