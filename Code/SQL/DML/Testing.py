print("===============================================================")
print("Testing data")
print("===============================================================")

import mysql.connector
from mysql.connector import Error

#===============================================================
# SQL Functions
#===============================================================

def create_server_connection(host_name, port,user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port= port
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return 0, None
    except mysql.connector.Error as err:
        if (err.errno == 1062):
            #print("Cannot insert, duplicate entry")
            return 1, err.msg
        elif(err.errno == 1292):
            #print("Incorrect value")
            return 2, err.msg
        elif(err.errno == 4025):
            #print("Incorrect value")
            return 3, err.msg
        elif(err.errno == 1265):
            #print("Incorrect value")
            return 4, err.msg
        else:
            print(f"Error: '{err}'")
            print(f"Query: '{query}'")
            

def getQueryResults(connection, IDquery):
    execute_query(connection, "USE Airport_DB;")
    cursor = connection.cursor()
    try:
        cursor.execute(IDquery)
        table = cursor.fetchall()
        #print(table)
        return([x[0] for x in table])
    except Error as err:
        print(f"Error: '{err}'")
        print(f"Query: '{IDquery}'")

def get_data(entry):
    output = (str(tuple(entry.keys())).replace("'",""), str(tuple(entry.values())))
    return output if output[0][-2]!= "," else (output[0][:-2]+output[0][-1],output[1][:-2]+output[1][-1])

def populate(connection, lst, target):
    for entry in lst:
        columns,values= get_data(entry)
        query = ("INSERT INTO "+ target+ " "+ columns+ " VALUES "+ values).replace("'null'","null")
        #print(query+"\n")
        return execute_query(connection, query)

#===============================================================
# Test data
#===============================================================

def testRemoveEmployee(dbConnection, employeeID):
    customerQuery = f"DELETE FROM Employee WHERE Employee_ID = {employeeID};"
    q2 = f"SELECT count(*) FROM (SELECT * From Employee Where Employee_ID = {employeeID}) AS count_of_query;"
    
    execute_query(dbConnection, "USE Airport_DB;")
    numOfResultsAtTheStart = getQueryResults(dbConnection, q2)[0]
    execute_query(dbConnection, customerQuery)
    numOfResultsAtTheEnd = getQueryResults(dbConnection, q2)[0]
    if(numOfResultsAtTheStart != numOfResultsAtTheEnd):
        return 0
    elif(numOfResultsAtTheStart == numOfResultsAtTheEnd):
        return 1

def testGetEmployeeID(dbConnection, employeeID):
    #print("===============================================================")
    #print("Testing employee retrieval of ID")
    #print("===============================================================")
    customerQuery = f"SELECT * FROM Employee Where Employee_ID = {employeeID};"
    customerIDs = getQueryResults(dbConnection, customerQuery)
    if(len(customerIDs) == 1):
        return(customerIDs[0])
    else:
        return(None)
    
def testGetParkingSpotID(dbConnection, parkingSpotID):
    customerQuery = f"SELECT * FROM CustomerParkingSpot Where Parking_Spot_ID = {parkingSpotID};"
    customerIDs = getQueryResults(dbConnection, customerQuery)
    if(len(customerIDs) == 1):
        return(customerIDs[0])
    else:
        return(None)
    
def testEmployeeInsertion(dbConnection, employeeID, hireDate, terminationDate, title, employmentType, salary, 
          supervisor, addressLine1, addressLine2, postcode, city, birthDate, parkingSpotFK, vehicleFK, departmentFK, manageDepartment):
    #print("===============================================================")
    #print("Testing employee insertion")
    #print("===============================================================")
    employees =[{
                "Employee_ID": employeeID,
                "Hire_Date": hireDate,
                "Termination_Date": terminationDate,
                "Title": title,
                "Employment_Type": employmentType,
                "Salary": salary,
                "Supervisor": supervisor,
                "Address_Line_1": addressLine1,
                "Address_Line_2": addressLine2,
                "Postcode": postcode,
                "City": city,
                "Birth_Date": birthDate,
                "Parking_Spot_FK": parkingSpotFK,
                "Vehicle_FK": vehicleFK,
                "Department_FK": departmentFK,
                "Manage_Department": manageDepartment,
            }]
        
    execute_query(dbConnection, "USE Airport_DB;")
    getEmployee = testGetEmployeeID(dbConnection, employeeID)
    tryInsertingEmployee = populate(dbConnection,employees,"Employee")
    if(getEmployee == None and tryInsertingEmployee[0] == 0): # There isn't an employee with that ID in the DB and execute_query returns 0 - no problem, this should be sucess
        #print("Employee successfully inserted")
        return 1, "Employee successfully inserted"
    elif(getEmployee == employeeID and tryInsertingEmployee[0] == 1): # If returned employeeID matches with inserted ID and execute_query returns 1 - employee already exists
        #print("Failed to insert employee, there is already an employee with this ID")
        return 2, "Failed to insert employee, there is already an employee with this ID"
    elif(getEmployee == None and tryInsertingEmployee[0] == 2):
        #print("Failed to insert employee, one of the attributes is in wrong type")
        #print(f"Incorrect value: {tryInsertingEmployee[1]}")
        return 3, "Failed to insert employee, one of the attributes is in wrong type", f"Incorrect value: {tryInsertingEmployee[1]}"
    elif(getEmployee == employeeID and tryInsertingEmployee[0] == 2):
        #print("Failed to insert employee, one of the attributes is in wrong type and there is already an employee with this ID")
        #print(f"Incorrect value: {tryInsertingEmployee[1]}")
        return 4, "Failed to insert employee, one of the attributes is in wrong type and there is already an employee with this ID", f"Incorrect value: {tryInsertingEmployee[1]}"
    else:
        print("Unknown error, read the error message:")
        print(tryInsertingEmployee[1])
        return 0
        
def testCustomerParkingInsertion(dbConnection, parkingSpotID, parkingType, pricePerHour):
    #print("===============================================================")
    #print("Testing employee insertion")
    #print("===============================================================")
    customer_parking_spots =[{
            "Parking_Spot_ID": parkingSpotID,
            "Parking_Type": parkingType,
            "Price_Per_Hour": pricePerHour
        }]
        
    execute_query(dbConnection, "USE Airport_DB;")
    getCustomerParking = testGetParkingSpotID(dbConnection, parkingSpotID)
    tryInsertingCustomer = populate(dbConnection, customer_parking_spots, "CustomerParkingSpot")

    if(getCustomerParking == None and tryInsertingCustomer[0] == 0): 
        return 1, "Customer parking spot successfully inserted"
    elif(getCustomerParking == parkingSpotID and tryInsertingCustomer[0] == 1): 
        return 2, "Failed to insert customer parking spot, there is already an customer parking spot with this ID"
    elif(getCustomerParking == None and tryInsertingCustomer[0] == 3):
        return 3, "Failed to insert customer parking spot, one of the attributes is in wrong type, check constraint", f"Incorrect value: {tryInsertingCustomer[1]}"  
    elif(getCustomerParking == parkingSpotID and tryInsertingCustomer[0] == 3):
        return 4, "Failed to insert customer parking spot, one of the attributes is in wrong type and there is already an customer parking spot with this ID, check constraint", f"Incorrect value: {tryInsertingCustomer[1]}"
    elif(getCustomerParking == None and tryInsertingCustomer[0] == 4):
        return 5, "Failed to insert customer parking spot, one of the attributes is in wrong type", f"Incorrect value: {tryInsertingCustomer[1]}"
    elif(getCustomerParking == parkingSpotID and tryInsertingCustomer[0] == 4):
        return 6, "Failed to insert customer parking spot, one of the attributes is in wrong type and there is already an customer parking spot with this ID", f"Incorrect value: {tryInsertingCustomer[1]}"
    else:
        print("Unknown error, read the error message:")
        print(tryInsertingCustomer[0])
        print(tryInsertingCustomer[1])
        return 0
    
#
def mainTest():
    connection = create_server_connection("localhost","30330", "my_user", "my_password")
    
    # Test1: 
    #       Task: try removing employees
    #       Expected result: 0 - employee 999999999 shouldn't be found
    test1 = testRemoveEmployee(connection, 999999999)
    if(test1 == 1):
        print("Test 1 pass: No employee was removed")
    else:
        print("Test 1 fail: Employee was removed")
    
    # Test2: 
    #       Task: get Employee data that matches 99999 from the DB
    #       Expected result: None - there shouldn't be an employee with this ID
    test2 = testGetEmployeeID(connection, 999999999)
    if(test2 == None):
        print("Test 2 pass: No employee was not found")
    else:
        print("Test 2 fail: Employee was found")
        
    # Test3: 
    #       Task: generate an employee
    #       Expected result: 1 - employee should be created   
    test3 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999999, hireDate = "2022-12-13", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test3[0] == 1):
        print(f"Test 3 pass: {test3[1]}")
    else:
        print("Test 3 fail")
          
    # Test4: 
    #       Task: fail to generate an employee based on duplicate ID
    #       Expected result: 2 - employee should be created   
    test4 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999999, hireDate = "2022-12-13", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test4[0] == 2):
        print(f"Test 4 pass: {test4[1]}")
    else:
        print("Test 4 fail")
        
    # Test5: 
    #       Task: fail to generate an employee based on wrong attribute - hireDate
    #       Expected result: 3 - employee should be created   
    test5 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999998, hireDate = "hireDate", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test5[0] == 3):
        print(f"Test 5 pass: {test5[1]} {test5[2]}")
    else:
        print("Test 5 fail")
        
    # Test6: 
    #       Task: fail to generate an employee based on duplicate ID and wrong attribute - hireDate
    #       Expected result: 4 - employee should be created   
    test6 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999999, hireDate = "hireDate", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test6[0] == 4):
        print(f"Test 6 pass: {test6[1]} {test6[2]}")
    else:
        print("Test 6 fail")
        
    # Test7: 
    #       Task: remove employee generated from above
    #       Expected result: 1 - employee 999999999 shall be removed   
    test7 = testRemoveEmployee(dbConnection = connection, employeeID = 999999999)
    if(test7 == 0):
        print("Test 7 pass: Employee was removed")
    else:
        print("Test 7 fail: No employee was removed")
        
    # Test8: 
    #       Task: generate a parking spot
    #       Expected result: 1 - parking spot should be created   
    test8 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6")
    if(test8[0] == 1):
        print(f"Test 8 pass: {test8[1]}")
    else:
        print("Test 8 fail")
    
    # Test9: 
    #       Task: fail to generate a customer parking spot based on duplicate ID
    #       Expected result: 2 - there shouldn't be an customer parking spot with this ID
    test9 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6")
    if(test9[0] == 2):
        print(f"Test 9 pass: {test9[1]}")
    else:
        print("Test 9 fail")
        
    # Test10: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 3 - under the limits
    #       Expected result: 3 - customer parking spot shouldn't be inserted due to constraints
    test10 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999997, parkingType = '{"1":" Car Parking "}' , pricePerHour = "3")
    if(test10[0] == 3):
        print(f"Test 10 pass: {test10[1]}")
    else:
        print("Test 10 fail")
        
    # Test11: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 3 - under the limits and ID of 999999999 is taken
    #       Expected result: 4 - customer parking spot shouldn't be inserted due to constraints and ID
    test11 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "3")
    if(test11[0] == 4):
        print(f"Test 11 pass: {test11[1]}")
    else:
        print("Test 11 fail")
        
    # Test12: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 400 - over the limits
    #       Expected result: 3 - customer parking spot shouldn't be inserted due to constraints  
    test12 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999997, parkingType = '{"1":" Car Parking "}' , pricePerHour = "400")
    if(test12[0] == 3):
        print(f"Test 12 pass: {test12[1]}")
    else:
        print("Test 12 fail")
        
    # Test13: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 400 - over the limits
    #       Expected result: 4 - customer parking spot shouldn't be inserted due to constraints
    test13 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "400")
    if(test13[0] == 4):
        print(f"Test 13 pass: {test13[1]}")
    else:
        print("Test 13 fail")
        
    # Test14: 
    #       Task: fail to generate a customer parking spot based on 6a being wrong type
    #       Expected result: 5 - failed to generate parking spot based on wrong type
    test14 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999997, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6a")
    if(test14[0] == 5):
        print(f"Test 14 pass: {test14[1]}")
    else:
        print("Test 14 fail")
        
    # Test15: 
    #       Task: fail to generate a customer parking spot based on 6a being wrong type and same ID
    #       Expected result: 6 - failed to generate parking spot based on wrong type and same ID
    test15 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6a")
    if(test15[0] == 6):
        print(f"Test 15 pass: {test15[1]}")
    else:
        print("Test 15 fail")
        
        
    
    
    
    
#===============================================================
# Insert dummy data
#===============================================================

mainTest()



#connection = create_server_connection("localhost","30330", "my_user", "my_password")
#testRemoveEmployee(connection,999999999)


#print(getCustomerParking)
#connection = create_server_connection("localhost","30330", "my_user", "my_password")


#testGetEmployeeID(connection, 99999)

'''
testEmployeeInsertion(dbConnection = connection, 
                    employeeID = 99999, 
                    hireDate = "2022-12-13", 
                    terminationDate = "2022-12-14", 
                    title = "Test_Title", 
                    employmentType = "Test_Employment", 
                    salary = 9000, 
                    supervisor = 5, 
                    addressLine1 = "Test_Address_Line_1", 
                    addressLine2 = "Test_Address_Line_2", 
                    postcode = "Test_Postcode", 
                    city = "Test_City", 
                    birthDate = "2022-11-14", 
                    parkingSpotFK = 17, 
                    vehicleFK = 21, 
                    departmentFK = 5, 
                    manageDepartment = "null")

'''