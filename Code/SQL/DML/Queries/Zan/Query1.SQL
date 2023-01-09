-- Query1

SELECT Customer_ID_To_Find
FROM
	(
		SELECT c.Customer_ID as Customer_ID_To_Find
		FROM Ticket t
		JOIN Customer c 
		ON t.Ticket_ID = c.Customer_ID 
		JOIN Flight f 
		ON t.Flight_FK = f.Flight_ID 
		ORDER BY f.Departure_Time ASC
		LIMIT 1
	) as FoundCustomerID;

CALL GetParkingToBePaid(2613);