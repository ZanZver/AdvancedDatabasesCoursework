--DDL code goes here!

-- Airline table
CREATE TABLE `Airline` (
  `Company_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Company_Name` varchar(100) NOT NULL,
  `Revenue` decimal(15,2) NOT NULL,
  PRIMARY KEY (`Company_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Compan Vehicle table
CREATE TABLE `CompanyVehicle` (
  `Vehicle_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Vehicle_Name` varchar(100) NOT NULL,
  `Vehicle_Driving_License_Requirement` varchar(100) NOT NULL,
  `Department_FK` int(11) NOT NULL,
  PRIMARY KEY (`Vehicle_ID`),
  KEY `CompanyVehicle_FK` (`Department_FK`),
  CONSTRAINT `CompanyVehicle_FK` FOREIGN KEY (`Department_FK`) REFERENCES `Department` (`Department_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Customer table
CREATE TABLE `Customer` (
  `Customer_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Express_Lane` tinyint(1) NOT NULL DEFAULT 0,
  `Token_FK` int(11) DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`),
  KEY `Customer_FK` (`Token_FK`),
  CONSTRAINT `Customer_FK` FOREIGN KEY (`Token_FK`) REFERENCES `ParkingToken` (`Token_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Department table
CREATE TABLE `Department` (
  `Department_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Department_Name` varchar(100) NOT NULL,
  `Department_Location` varchar(100) NOT NULL,
  PRIMARY KEY (`Department_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Employee table
CREATE TABLE `Employee` (
  `Employee_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Hire_Date` date NOT NULL,
  `Termination_Date` date NOT NULL,
  `Title` varchar(100) NOT NULL,
  `Employment_Type` varchar(100) NOT NULL,
  `Salary` decimal(15,2) NOT NULL,
  `Supervisor` int(11) DEFAULT NULL COMMENT 'ID of the Employee that is supervisor',
  `AddressLine1` varchar(100) NOT NULL,
  `AddressLine2` varchar(100) DEFAULT NULL,
  `Postcode` varchar(100) NOT NULL,
  `City` varchar(100) NOT NULL,
  `BirthDate` date NOT NULL,
  `Parking_Spot_FK` int(11) DEFAULT NULL,
  `Vehicle_FK` int(11) DEFAULT NULL,
  `Department_FK` int(11) NOT NULL,
  `Manage_Department` int(11) DEFAULT NULL,
  PRIMARY KEY (`Employee_ID`),
  KEY `Employee_FK` (`Parking_Spot_FK`),
  KEY `Employee_FK_1` (`Vehicle_FK`),
  KEY `Employee_FK_2` (`Department_FK`),
  KEY `Employee_FK_3` (`Supervisor`),
  KEY `Employee_FK_4` (`Manage_Department`),
  CONSTRAINT `Employee_FK` FOREIGN KEY (`Parking_Spot_FK`) REFERENCES `ParkingSpot` (`Parking_Spot_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_FK_1` FOREIGN KEY (`Vehicle_FK`) REFERENCES `CompanyVehicle` (`Vehicle_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_FK_2` FOREIGN KEY (`Department_FK`) REFERENCES `Department` (`Department_ID`),
  CONSTRAINT `Employee_FK_3` FOREIGN KEY (`Supervisor`) REFERENCES `Employee` (`Employee_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Employee_FK_4` FOREIGN KEY (`Manage_Department`) REFERENCES `Department` (`Department_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='Storing employee details';

-- Flight table
CREATE TABLE `Flight` (
  `Flight_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Plane_Model` varchar(100) NOT NULL,
  `Departure_Time` datetime NOT NULL,
  `Destination` varchar(100) NOT NULL,
  `Gate` varchar(100) NOT NULL,
  `Runway_FK` int(11) NOT NULL,
  `Airline_FK` int(11) NOT NULL,
  PRIMARY KEY (`Flight_ID`),
  KEY `Flight_FK` (`Runway_FK`),
  KEY `Flight_FK_1` (`Airline_FK`),
  CONSTRAINT `Flight_FK` FOREIGN KEY (`Runway_FK`) REFERENCES `Runway` (`Runway_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Flight_FK_1` FOREIGN KEY (`Airline_FK`) REFERENCES `Airline` (`Company_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Person Name table
CREATE TABLE `Name` (
  `First_Name` varchar(100) NOT NULL,
  `Middle_Name` varchar(100) DEFAULT NULL,
  `Last_Name` varchar(100) NOT NULL,
  `Person_ID` int(11) NOT NULL,
  KEY `Name_FK_1` (`Person_ID`),
  CONSTRAINT `Name_FK` FOREIGN KEY (`Person_ID`) REFERENCES `Customer` (`Customer_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Name_FK_1` FOREIGN KEY (`Person_ID`) REFERENCES `Employee` (`Employee_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Parking Token table
CREATE TABLE `ParkingToken` (
  `Token_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Date` datetime NOT NULL,
  PRIMARY KEY (`Token_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Runway table
CREATE TABLE `Runway` (
  `Runway_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Length` decimal(10,0) NOT NULL,
  `Width` decimal(10,0) NOT NULL,
  PRIMARY KEY (`Runway_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Ticket table
CREATE TABLE `Ticket` (
  `Ticket_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_FK` int(11) NOT NULL,
  `Flight_FK` int(11) NOT NULL,
  PRIMARY KEY (`Ticket_ID`),
  KEY `Ticket_FK` (`Flight_FK`),
  KEY `Ticket_FK_1` (`Customer_FK`),
  CONSTRAINT `Ticket_FK` FOREIGN KEY (`Flight_FK`) REFERENCES `Flight` (`Flight_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Ticket_FK_1` FOREIGN KEY (`Customer_FK`) REFERENCES `Customer` (`Customer_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Parking Spot table
CREATE TABLE `ParkingSpot` (
  `Parking_Spot_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Parking_Type` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`Parking_Type`)),
  PRIMARY KEY (`Parking_Spot_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Qualification table
CREATE TABLE `Qualification` (
  `Qualification_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Qualification_Type` varchar(100) NOT NULL,
  `Qualification_Name` varchar(100) NOT NULL,
  PRIMARY KEY (`Qualification_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- Certificate table
CREATE TABLE `Certificate` (
  `Employee_FK` int(11) NOT NULL,
  `Certificate_ID` int(11) NOT NULL,
  `Certificate_Name` varchar(100) NOT NULL,
  `Achievement_Level` varchar(100) NOT NULL,
  `Qualification_FK` int(11) DEFAULT NULL,
  PRIMARY KEY (`Certificate_ID`),
  KEY `Certificate_FK` (`Employee_FK`),
  KEY `Certificate_FK_1` (`Qualification_FK`),
  CONSTRAINT `Certificate_FK` FOREIGN KEY (`Employee_FK`) REFERENCES `Employee` (`Employee_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Certificate_FK_1` FOREIGN KEY (`Qualification_FK`) REFERENCES `Qualification` (`Qualification_ID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;