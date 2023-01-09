-- Optimization technique

-- Person Name table
CREATE TABLE `Name` (
  `Person_ID` int(11) NOT NULL,
  `First_Name` varchar(48) NOT NULL,
  `Middle_Name` varchar(48) DEFAULT NULL,
  `Last_Name` varchar(48) NOT NULL,
  `Is_Employee` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Data needs to be 0 (default) if person is not employee or 1 if they are employee',
  PRIMARY KEY (`Person_ID`,`Is_Employee`),
  CHECK(`Is_Employee`<=1 or `Is_Employee`>=0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3
PARTITION BY RANGE (Is_Employee)
(
	PARTITION Customer_Partition VALUES LESS THAN (1),
	PARTITION Employee_Partition VALUES LESS THAN (2)
);