/*
================================================================================================================================================
        Procedure of price that needs to be paid for parking
================================================================================================================================================
*/

CREATE DEFINER=`my_user`@`%` PROCEDURE `Airport_DB`.`GetParkingToBePaid`()
BEGIN
	SELECT c.Customer_ID
       , pt.Token_ID
       , pt.`Date`
       , cps.*
       , cps.Price_Per_Hour * (SELECT TIMESTAMPDIFF(HOUR, pt.`Date` , CURRENT_TIMESTAMP) * (30 / 60) ) as ToPay
	FROM Customer c
	INNER JOIN ParkingToken pt 
	ON c.Token_FK = pt.Token_ID
	INNER JOIN CustomerParkingSpot cps 
	ON cps.Parking_Spot_ID = pt.Token_ID;
END;