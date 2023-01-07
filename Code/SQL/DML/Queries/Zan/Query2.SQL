-- Query2

SELECT e.Employee_ID, Supervisors.Supervises, e.Salary, en.First_Name, en.Last_Name, en.Middle_Name
FROM 
	(
		SELECT Supervisor, COUNT(*) as Supervises
		FROM Employee
		GROUP BY Supervisor
	) as Supervisors
JOIN Employee e 
ON Supervisors.Supervisor = e.Employee_ID
JOIN EmployeeNames en 
ON Supervisors.Supervisor = en.Person_ID
ORDER BY Supervisors.Supervises DESC, e.Salary DESC;