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
  `Certificate_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Employee_FK` int(11) NOT NULL,
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
  `Title` varchar(48) NOT NULL,
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
  CHECK(`Length`>=2000 and `Length`<=4000),
  CHECK(`Width`>=8 and `Width`<=80)
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
-- ALTER TABLE Airport_DB.Name ADD CONSTRAINT Name_FK_Customer FOREIGN KEY (Person_ID) REFERENCES Airport_DB.Customer(Customer_ID) ON DELETE CASCADE ON UPDATE CASCADE;
-- ALTER TABLE Airport_DB.Name ADD CONSTRAINT Name_FK_Employee FOREIGN KEY (Person_ID) REFERENCES Airport_DB.Employee(Employee_ID) ON DELETE CASCADE ON UPDATE CASCADE;

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