CREATE DATABASE hotel_db;
USE hotel_db;

CREATE TABLE Guests (
    guest_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_name VARCHAR(255) NOT NULL,
    passport VARCHAR(50) NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE Employees (
    employees_id INT AUTO_INCREMENT PRIMARY KEY,
    employees_name VARCHAR(255) NOT NULL,
    position VARCHAR(100),
    phone VARCHAR(20)
);

CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL,
    type_room VARCHAR(50)
);

CREATE TABLE Bookings (
    bookings_id INT AUTO_INCREMENT PRIMARY KEY,
    guest_book_id INT,
    room_book_id INT,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    employee_book_id INT,
    FOREIGN KEY (guest_book_id) REFERENCES Guests(guest_id),
    FOREIGN KEY (room_book_id) REFERENCES Rooms(room_id),
    FOREIGN KEY (employee_book_id) REFERENCES Employees(employees_id)
);

INSERT INTO Guests (guest_name, passport, phone) VALUES
('Иван Иванов', '1234567890', '+79991234567'),
('Мария Петрова', '0987654321', '+79997654321');

INSERT INTO Employees (employees_name, position, phone) VALUES
('Илья Каржановский', 'Администратор', '+79991112233'),
('Кирилл Ковалев', 'Менеджер', '+79993334455');

INSERT INTO Rooms (room_number, type_room) VALUES
('101', 'Стандарт'),
('102', 'Люкс');

INSERT INTO Bookings (guest_book_id, room_book_id, check_in_date, check_out_date, employee_book_id) VALUES
(1, 1, '2025-05-20', '2025-05-25', 1),
(2, 2, '2025-06-01', '2025-06-05', 2);


UPDATE Employees
SET employees_name = 'Кирилл Ковалев'
WHERE employees_id = 2;