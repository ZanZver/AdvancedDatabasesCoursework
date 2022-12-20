--DDL code goes here!

-- 
CREATE TABLE Airport_DB.Employee (
	Employee_ID INT auto_increment NOT NULL,
	Hire_Date DATE NOT NULL,
	Termination_Date DATE NOT NULL,
	Title varchar(100) NOT NULL,
	Employment_Type varchar(100) NOT NULL,
	Salary DECIMAL(15,2) NOT NULL,
	Supervisor varchar(100) NULL COMMENT 'ID of the Employee that is supervisor',
	AddressLine1 varchar(100) NOT NULL,
	AddressLine2 varchar(100) NULL,
	Postcode varchar(100) NOT NULL,
	City varchar(100) NOT NULL,
	BirthDate DATE NOT NULL,
	CONSTRAINT Employee_PK PRIMARY KEY (Employee_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci
COMMENT='Storing employee details';

-- 
CREATE TABLE Airport_DB.Department (
	Department_ID INT NULL AUTO_INCREMENT,
	Department_Name varchar(100) NOT NULL,
	Department_Location varchar(100) NOT NULL,
	CONSTRAINT Department_PK PRIMARY KEY (Department_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.CompanyVehicle (
	Vehicle_ID INT auto_increment NOT NULL,
	Vehicle_Name varchar(100) NOT NULL,
	Vehicle_Driving_License_Requirement varchar(100) NOT NULL,
	CONSTRAINT CompanyVehicle_PK PRIMARY KEY (Vehicle_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.Airline (
	Company_ID INT auto_increment NOT NULL,
	Company_Name varchar(100) NOT NULL,
	Revenue DECIMAL(15,2) NOT NULL,
	CONSTRAINT Airline_PK PRIMARY KEY (Company_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

CREATE TABLE Airport_DB.Runway (
	Runway_ID INT auto_increment NOT NULL,
	`Length` DECIMAL NOT NULL,
	Width varchar(100) NOT NULL,
	CONSTRAINT Runway_PK PRIMARY KEY (Runway_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.Flight (
	Flight_ID INT auto_increment NOT NULL,
	Plane_Model varchar(100) NOT NULL,
	Departure_Time DATETIME NOT NULL,
	Destination varchar(100) NOT NULL,
	Gate varchar(100) NOT NULL,
	CONSTRAINT Flight_PK PRIMARY KEY (Flight_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.Ticket (
	Ticket_ID INT auto_increment NOT NULL,
	CONSTRAINT Ticket_PK PRIMARY KEY (Ticket_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.Customer (
	Customer_ID INT auto_increment NOT NULL,
	Express_Lane BOOL DEFAULT false NOT NULL,
	CONSTRAINT Customer_PK PRIMARY KEY (Customer_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.ParkingToken (
	Token_ID INT auto_increment NOT NULL,
	`Date` DATETIME NOT NULL,
	CONSTRAINT ParkingToken_PK PRIMARY KEY (Token_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.Name (
  First_Name varchar(100) NOT NULL,
  Middle_Name varchar(100) DEFAULT NULL,
  Last_Name varchar(100) NOT NULL
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;

-- 
CREATE TABLE Airport_DB.ParkingSpot (
	Parking_Spot_ID INT auto_increment NOT NULL,
	Parking_Type json NOT NULL,
	CONSTRAINT ParkingSpot_PK PRIMARY KEY (Parking_Spot_ID)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb3
COLLATE=utf8mb3_general_ci;