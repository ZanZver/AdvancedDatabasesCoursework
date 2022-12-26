/*
================================================================================================================================================
        Specify use of Airport_DB database
================================================================================================================================================
*/

USE Airport_DB;

/*
================================================================================================================================================
        Create tables
================================================================================================================================================
*/

-- Airline table
CREATE TABLE `Airline` (
  `Company_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Company_Name` varchar(64) NOT NULL,
  `Revenue` decimal(15,2) NOT NULL COMMENT 'Revenue needs to be at least 10000 per month',
  PRIMARY KEY (`Company_ID`),
  CHECK(`Revenue`>=10000)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Certificate table
CREATE TABLE `Certificate` (
  `Employee_FK` int(11) NOT NULL,
  `Certificate_ID` int(11) NOT NULL,
  `Certificate_Name` varchar(64) NOT NULL,
  `Achievement_Level` varchar(32) NOT NULL,
  `Qualification_FK` int(11) DEFAULT NULL,
  PRIMARY KEY (`Certificate_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Compan Vehicle table
CREATE TABLE `CompanyVehicle` (
  `Vehicle_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Vehicle_Name` varchar(48) NOT NULL,
  `Vehicle_Driving_License_Requirement` varchar(24) NOT NULL,
  `Department_FK` int(11) NOT NULL,
  PRIMARY KEY (`Vehicle_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Customer table
CREATE TABLE `Customer` (
  `Customer_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Express_Lane` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Data needs to be 0 (default) if there is no express lane or 1 if user has express lane',
  `Token_FK` int(11) DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`),
  CHECK(`Express_Lane`<=1 or `Express_Lane`>=0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Customer Parking Spot table
CREATE TABLE `CustomerParkingSpot` (
  `Parking_Spot_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parking_Type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`Parking_Type`)),
  `Price_Per_Hour` decimal(15,2) NOT NULL COMMENT 'Minimum pricing per hour is £5 and maximum is £300',
  PRIMARY KEY (`Parking_Spot_ID`),
  CHECK(`Price_Per_Hour`>=5 and `Price_Per_Hour`<=300)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Department table
CREATE TABLE `Department` (
  `Department_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Department_Name` varchar(32) NOT NULL,
  `Department_Location` varchar(24) NOT NULL,
  PRIMARY KEY (`Department_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Employee table
CREATE TABLE `Employee` (
  `Employee_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hire_Date` date NOT NULL,
  `Termination_Date` date NULL,
  `Title` varchar(24) NOT NULL,
  `Employment_Type` varchar(24) NOT NULL,
  `Salary` decimal(15,2) NOT NULL COMMENT 'Salary is minimum of 2160 per year. Person is paid £9/h (minimum) * 5h (minimum per week) * 4 (whole month) * 12 (months in year) = 2160',
  `Supervisor` int(11) DEFAULT NULL COMMENT 'ID of the Employee that is supervisor',
  `Address_Line_1` varchar(48) NOT NULL,
  `Address_Line_2` varchar(48) DEFAULT NULL,
  `Postcode` varchar(32) NOT NULL,
  `City` varchar(48) NOT NULL,
  `Birth_Date` date NOT NULL,
  `Parking_Spot_FK` int(11) DEFAULT NULL,
  `Vehicle_FK` int(11) DEFAULT NULL,
  `Department_FK` int(11) NOT NULL,
  `Manage_Department` int(11) DEFAULT NULL,
  PRIMARY KEY (`Employee_ID`),
  CHECK(`Salary`>=2160)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='Storing employee details';

-- Employee Parking Spot table
CREATE TABLE `EmployeeParkingSpot` (
  `Parking_Spot_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parking_Type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`Parking_Type`)),
  PRIMARY KEY (`Parking_Spot_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Flight table
CREATE TABLE `Flight` (
  `Flight_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Plane_Model` varchar(64) NOT NULL,
  `Departure_Time` datetime NOT NULL,
  `Destination` varchar(48) NOT NULL,
  `Gate` varchar(24) NOT NULL,
  `Runway_FK` int(11) NOT NULL,
  `Airline_FK` int(11) NOT NULL,
  PRIMARY KEY (`Flight_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Person Name table
CREATE TABLE `Name` (
  `Person_ID` int(11) NOT NULL,
  `First_Name` varchar(48) NOT NULL,
  `Middle_Name` varchar(48) DEFAULT NULL,
  `Last_Name` varchar(48) NOT NULL,
  `Is_Employee` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Data needs to be 0 (default) if person is not employee or 1 if they are employee',
  PRIMARY KEY (`Person_ID`,`Is_Employee`),
  CHECK(`Is_Employee`<=1 or `Is_Employee`>=0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*
PARTITION BY RANGE (`Is_Employee`) (
    PARTITION p0 VALUES LESS THAN (0),
    PARTITION p1 VALUES LESS THAN (1),
    PARTITION p2 VALUES LESS THAN (2)
);*/

-- Parking Token table
CREATE TABLE `ParkingToken` (
  `Token_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Date` datetime NOT NULL,
  `Parking_Spot_FK` int(11) NOT NULL,
  PRIMARY KEY (`Token_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Runway table
CREATE TABLE `Runway` (
  `Runway_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Length` decimal(10,0) NOT NULL COMMENT 'Length needs to be at least 10, combined with Width it can be helipad. Longest it can be is 3km.',
  `Width` decimal(10,0) NOT NULL COMMENT 'Width needs to be at least 10, combined with Length it can be helipad. Max width acceptable is 500m.',
  PRIMARY KEY (`Runway_ID`),
  CHECK(`Length`>=10 and `Length`<=3000),
  CHECK(`Width`>=10 and `Width`<=500)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Ticket table
CREATE TABLE `Ticket` (
  `Ticket_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_FK` int(11) NOT NULL,
  `Flight_FK` int(11) NOT NULL,
  PRIMARY KEY (`Ticket_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Qualification table
CREATE TABLE `Qualification` (
  `Qualification_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Qualification_Type` varchar(48) NOT NULL,
  `Qualification_Name` varchar(48) NOT NULL,
  PRIMARY KEY (`Qualification_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


/*
================================================================================================================================================
        Add Temp Data
================================================================================================================================================
*/

-- Airline table
INSERT INTO Airport_DB.Airline (Company_ID, Company_Name, Revenue) 
VALUES (1, 'Company_1', 20000.00);
INSERT INTO Airport_DB.Airline (Company_ID, Company_Name, Revenue) 
VALUES (2, 'Company_2', 40000.00);
INSERT INTO Airport_DB.Airline (Company_ID, Company_Name, Revenue) 
VALUES (3, 'Company_3', 80000.00);

-- Certificate table
INSERT INTO Airport_DB.Certificate (Employee_FK, Certificate_ID, Certificate_Name, Achievement_Level, Qualification_FK) 
VALUES (1, 1, 'Certificate_1', 'Achievement_1', 1);
INSERT INTO Airport_DB.Certificate (Employee_FK, Certificate_ID, Certificate_Name, Achievement_Level, Qualification_FK) 
VALUES (1, 2, 'Certificate_2', 'Achievement_2', 2);
INSERT INTO Airport_DB.Certificate (Employee_FK, Certificate_ID, Certificate_Name, Achievement_Level, Qualification_FK) 
VALUES (2, 3, 'Certificate_1', 'Achievement_3', 3);

-- Company Vehicle table
INSERT INTO Airport_DB.CompanyVehicle (Vehicle_ID, Vehicle_Name, Vehicle_Driving_License_Requirement, Department_FK) 
VALUES (1, 'Vehicle_1', 'License_1', 1);
INSERT INTO Airport_DB.CompanyVehicle (Vehicle_ID, Vehicle_Name, Vehicle_Driving_License_Requirement, Department_FK) 
VALUES (2, 'Vehicle_2', 'License_1', 1);
INSERT INTO Airport_DB.CompanyVehicle (Vehicle_ID, Vehicle_Name, Vehicle_Driving_License_Requirement, Department_FK) 
VALUES (3, 'Vehicle_3', 'License_2', 2);

-- Customer table
INSERT INTO Airport_DB.Customer (Customer_ID, Express_Lane, Token_FK) 
VALUES (1, 0, 1);
INSERT INTO Airport_DB.Customer (Customer_ID, Express_Lane, Token_FK) 
VALUES (2, 1, 2);
INSERT INTO Airport_DB.Customer (Customer_ID, Express_Lane) 
VALUES (3, 0);

-- Customer Parking Spot table
INSERT INTO Airport_DB.CustomerParkingSpot (Parking_Spot_ID, Parking_Type, Price_Per_Hour) 
VALUES (1, '{"1":"Car Parking"}', 6);
INSERT INTO Airport_DB.CustomerParkingSpot (Parking_Spot_ID, Parking_Type, Price_Per_Hour) 
VALUES (2, '{"1":"Motor Parking"}', 6);
INSERT INTO Airport_DB.CustomerParkingSpot (Parking_Spot_ID, Parking_Type, Price_Per_Hour) 
VALUES (3, '{"1":"Car Parking", "2":"Handicap parking"}', 5);

-- Department table
INSERT INTO Airport_DB.Department (Department_ID, Department_Name, Department_Location) 
VALUES (1, 'Department_1', 'Location_1');
INSERT INTO Airport_DB.Department (Department_ID, Department_Name, Department_Location) 
VALUES (2, 'Department_2', 'Location_2');
INSERT INTO Airport_DB.Department (Department_ID, Department_Name, Department_Location) 
VALUES (3, 'Department_3', 'Location_3');

-- Employee table
INSERT INTO Airport_DB.Employee (Employee_ID, Hire_Date, Termination_Date, Title, Employment_Type, Salary, Supervisor, Address_Line_1, Address_Line_2, Postcode, City, Birth_Date, Parking_Spot_FK, Vehicle_FK, Department_FK, Manage_Department) 
VALUES (1, '2022-1-1', null, 'Title_1', 'Type_1', 90000, null, 'Address_Line_1_1', null, 'Postcode_1', 'City_1', '1980-12-1', 1, 1, 1, 1);
INSERT INTO Airport_DB.Employee (Employee_ID, Hire_Date, Termination_Date, Title, Employment_Type, Salary, Supervisor, Address_Line_1, Address_Line_2, Postcode, City, Birth_Date, Parking_Spot_FK, Vehicle_FK, Department_FK, Manage_Department) 
VALUES (2, '2022-2-2', '2022-12-31', 'Title_2', 'Type_2', 60000, 1, 'Address_Line_1_2', 'Address_Line_2_2', 'Postcode_2', 'City_2', '1980-12-3', 2, 2, 2, 2);
INSERT INTO Airport_DB.Employee (Employee_ID, Hire_Date, Termination_Date, Title, Employment_Type, Salary, Supervisor, Address_Line_1, Address_Line_2, Postcode, City, Birth_Date, Parking_Spot_FK, Vehicle_FK, Department_FK, Manage_Department) 
VALUES (3, '2022-3-3', null, 'Title_3', 'Type_3', 30000, 2, 'Address_Line_1_3', null, 'Postcode_3', 'City_3', '1980-12-3', 2, null, 2, null);

-- Employee Parking Spot table
INSERT INTO Airport_DB.EmployeeParkingSpot (Parking_Spot_ID, Parking_Type)
VALUES (1, '{"1":"Car Parking", "2":"CEO parking"}');
INSERT INTO Airport_DB.EmployeeParkingSpot (Parking_Spot_ID, Parking_Type)
VALUES (2, '{"1":"Motor Parking"}');
INSERT INTO Airport_DB.EmployeeParkingSpot (Parking_Spot_ID, Parking_Type)
VALUES (3, '{"1":"Car Parking", "2":"Handicap parking"}');

-- Flight table
INSERT INTO Airport_DB.Flight (Flight_ID, Plane_Model, Departure_Time, Destination, Gate, Runway_FK, Airline_FK)
VALUES (1, 'Model_1', '2022-01-10 01:00:00', 'Destination_1', 'Gate_1', 1, 1);
INSERT INTO Airport_DB.Flight (Flight_ID, Plane_Model, Departure_Time, Destination, Gate, Runway_FK, Airline_FK)
VALUES (2, 'Model_2', '2022-02-20 22:22:00', 'Destination_2', 'Gate_2', 1, 2);
INSERT INTO Airport_DB.Flight (Flight_ID, Plane_Model, Departure_Time, Destination, Gate, Runway_FK, Airline_FK)
VALUES (3, 'Model_3', '2022-03-30 09:30:00', 'Destination_3', 'Gate_3', 2, 2);

-- Name table
INSERT INTO Airport_DB.Name (Person_ID, First_Name, Middle_Name, Last_Name, Is_Employee)
VALUES (1, 'FN_1', null, 'LN_1', 1);
INSERT INTO Airport_DB.Name (Person_ID, First_Name, Middle_Name, Last_Name, Is_Employee)
VALUES (2, 'FN_2', 'MN_2', 'LN_2', 1);
INSERT INTO Airport_DB.Name (Person_ID, First_Name, Middle_Name, Last_Name, Is_Employee)
VALUES (3, 'FN_3', null, 'LN_3', 1);
INSERT INTO Airport_DB.Name (Person_ID, First_Name, Middle_Name, Last_Name, Is_Employee)
VALUES (1, 'FN_4', 'MN_4', 'LN_4', 0);
INSERT INTO Airport_DB.Name (Person_ID, First_Name, Middle_Name, Last_Name, Is_Employee)
VALUES (2, 'FN_5', 'MN_5', 'LN_5', 0);
INSERT INTO Airport_DB.Name (Person_ID, First_Name, Middle_Name, Last_Name, Is_Employee)
VALUES (3, 'FN_6', null, 'LN_6', 0);

-- Parking Token table
INSERT INTO Airport_DB.ParkingToken (Token_ID, `Date`, Parking_Spot_FK)
VALUES (1, '2022-01-10 11:11:00',1);
INSERT INTO Airport_DB.ParkingToken (Token_ID, `Date`, Parking_Spot_FK)
VALUES (2, '2022-02-20 22:00:00',2);
INSERT INTO Airport_DB.ParkingToken (Token_ID, `Date`, Parking_Spot_FK)
VALUES (3, '2022-03-30 15:30:00',3);

-- Runway table
INSERT INTO Airport_DB.Runway (Runway_ID, `Length`, Width)
VALUES (1, 100, 10);
INSERT INTO Airport_DB.Runway (Runway_ID, `Length`, Width)
VALUES (2, 200, 20);
INSERT INTO Airport_DB.Runway (Runway_ID, `Length`, Width)
VALUES (3, 300, 30);

-- Ticket table
INSERT INTO Airport_DB.Ticket (Ticket_ID, Customer_FK, Flight_FK)
VALUES (1, 1, 1);
INSERT INTO Airport_DB.Ticket (Ticket_ID, Customer_FK, Flight_FK)
VALUES (2, 2, 1);
INSERT INTO Airport_DB.Ticket (Ticket_ID, Customer_FK, Flight_FK)
VALUES (3, 3, 3);

-- Qualification table
INSERT INTO Airport_DB.Qualification (Qualification_ID, Qualification_Type, Qualification_Name)
VALUES (1, "Type_1", "Name_1");
INSERT INTO Airport_DB.Qualification (Qualification_ID, Qualification_Type, Qualification_Name)
VALUES (2, "Type_2", "Name_2");
INSERT INTO Airport_DB.Qualification (Qualification_ID, Qualification_Type, Qualification_Name)
VALUES (3, "Type_3", "Name_3");

/*
================================================================================================================================================
        Add foregin keys
================================================================================================================================================
*/

-- Certificate table
ALTER TABLE Airport_DB.Certificate ADD CONSTRAINT Certificate_FK_Employee FOREIGN KEY (Employee_FK) REFERENCES Airport_DB.Employee(Employee_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE Airport_DB.Certificate ADD CONSTRAINT Certificate_FK_Qualification FOREIGN KEY (Qualification_FK) REFERENCES Airport_DB.Qualification(Qualification_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Company vehicle table
ALTER TABLE Airport_DB.CompanyVehicle ADD CONSTRAINT CompanyVehicle_FK_Department FOREIGN KEY (Department_FK) REFERENCES Airport_DB.Department(Department_ID) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- Certificate table
ALTER TABLE Airport_DB.Customer ADD CONSTRAINT Customer_FK_ParkingToken FOREIGN KEY (Token_FK) REFERENCES Airport_DB.ParkingToken(Token_ID);

-- Employee table
ALTER TABLE Airport_DB.Employee ADD CONSTRAINT Employee_FK_EmployeeParkingSpot FOREIGN KEY (Parking_Spot_FK) REFERENCES Airport_DB.EmployeeParkingSpot(Parking_Spot_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Employee ADD CONSTRAINT Employee_FK_CompanyVehicle FOREIGN KEY (Vehicle_FK) REFERENCES Airport_DB.CompanyVehicle(Vehicle_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Employee ADD CONSTRAINT Employee_FK_DepartmentID FOREIGN KEY (Department_FK) REFERENCES Airport_DB.Department(Department_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Employee ADD CONSTRAINT Employee_FK_DepartmentManage FOREIGN KEY (Manage_Department) REFERENCES Airport_DB.Department(Department_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Employee ADD CONSTRAINT Employee_FK_Employee FOREIGN KEY (Supervisor) REFERENCES Airport_DB.Employee(Employee_ID) ON DELETE CASCADE ON UPDATE CASCADE;

-- Flight table
ALTER TABLE Airport_DB.Flight ADD CONSTRAINT Flight_FK_Runway FOREIGN KEY (Runway_FK) REFERENCES Airport_DB.Runway(Runway_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Flight ADD CONSTRAINT Flight_FK_Airline FOREIGN KEY (Airline_FK) REFERENCES Airport_DB.Airline(Company_ID) ON DELETE CASCADE ON UPDATE CASCADE;

-- Name table
ALTER TABLE Airport_DB.Name ADD CONSTRAINT Name_FK_Customer FOREIGN KEY (Person_ID) REFERENCES Airport_DB.Customer(Customer_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Name ADD CONSTRAINT Name_FK_Employee FOREIGN KEY (Person_ID) REFERENCES Airport_DB.Employee(Employee_ID) ON DELETE CASCADE ON UPDATE CASCADE;

-- Ticket table
ALTER TABLE Airport_DB.Ticket ADD CONSTRAINT Ticket_FK_Flight FOREIGN KEY (Flight_FK) REFERENCES Airport_DB.Flight(Flight_ID) ON DELETE CASCADE ON UPDATE CASCADE;
ALTER TABLE Airport_DB.Ticket ADD CONSTRAINT Ticket_FK_Customer FOREIGN KEY (Customer_FK) REFERENCES Airport_DB.Customer(Customer_ID) ON DELETE CASCADE ON UPDATE CASCADE;

/*
================================================================================================================================================
        Create views
================================================================================================================================================
*/

CREATE VIEW CustomerNames AS
SELECT Person_ID, First_Name, Middle_Name, Last_Name
FROM Name n
WHERE n.Is_Employee = 0;

CREATE VIEW EmployeeNames AS
SELECT Person_ID, First_Name, Middle_Name, Last_Name
FROM Name n
WHERE n.Is_Employee = 1;