-- Query3

SELECT Destination, Company_Name, Revenue -- Get just the 3 required attributes
FROM (
    SELECT 
    	f.Destination as Destination, 
    	a.Company_Name as Company_Name,
    	a.Revenue as Revenue,
        ROW_NUMBER() OVER (PARTITION BY Company_Name Order by Revenue ASC) AS RowID -- Partition city based on price and save this as RowID
    FROM Flight f 
	JOIN Airline a 
	ON f.Airline_FK = a.Company_ID
)RNK
WHERE RowID <= 3
ORDER BY Revenue DESC;