/*
================================================================================================================================================
        Procedure of price that needs to be paid for parking
================================================================================================================================================
*/


/*
================================================================================================================================================
        Create procedure
================================================================================================================================================
*/
CREATE DEFINER=`my_user`@`%` 
PROCEDURE `Airport_DB`.`GetParkingToBePaid2` (Filter_Customer_ID int(11))
BEGIN
	SELECT c.Customer_ID
          , pt.Token_ID
          , pt.`Date`
          , cps.*
          , cps.Price_Per_Hour * (SELECT TIMESTAMPDIFF
            (HOUR, pt.`Date` , CURRENT_TIMESTAMP)
            * (30 / 60) ) as ToPay
	FROM Customer c
	INNER JOIN ParkingToken pt 
	ON c.Token_FK = pt.Token_ID
	INNER JOIN CustomerParkingSpot cps 
	ON cps.Parking_Spot_ID = pt.Token_ID
	WHERE c.Customer_ID = Filter_Customer_ID;
END;

/*
================================================================================================================================================
        Call procedure
================================================================================================================================================
*/
-- Replace Customer_ID with desired ID
CALL Airport_DB.GetParkingToBePaid2(Customer_ID);