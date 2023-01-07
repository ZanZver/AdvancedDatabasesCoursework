print("===============================================================")
print("Unit testing database")
print("===============================================================")

import mysql.connector
from mysql.connector import Error

#===============================================================
# SQL Functions
#===============================================================

def create_server_connection(host_name, port,user_name, user_password):
    '''
        Return connection (if made), error code (if made) and error (if made)
    '''
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port= port
        )
        return connection, None, None
    except mysql.connector.Error as err:
        if (err.errno == 2003):
            return None, 1, None
        elif(err.errno == 1045):
            return None, 2, None
        else:    
            print(f"Error: '{err}'")
            return None, 0, err

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
        return([x[0] for x in table])
    except Error as err:
        print(f"Error: '{err}'")
        print(f"Query: '{IDquery}'")

def get_data(entry):
    output = (str(tuple(entry.keys())).replace("'",""), str(tuple(entry.values())))
    return output if output[0][-2]!= "," else (output[0][:-2]+output[0][-1],output[1][:-2]+output[1][-1])

def populate(connection, lst, target):
    for entry in lst:
        columns, values= get_data(entry)
        query = ("INSERT INTO "+ target+ " "+ columns+ " VALUES "+ values).replace("'null'","null")
        return execute_query(connection, query)

#===============================================================
# Test functions
#===============================================================

def testRemoveEmployee(dbConnection, employeeID):
    removeQuery = f"DELETE FROM Employee WHERE Employee_ID = {employeeID};"
    countQuery = f"SELECT count(*) FROM (SELECT * From Employee Where Employee_ID = {employeeID}) AS count_of_query;"
    
    execute_query(dbConnection, "USE Airport_DB;")
    numOfResultsAtTheStart = getQueryResults(dbConnection, countQuery)[0]
    execute_query(dbConnection, removeQuery)
    numOfResultsAtTheEnd = getQueryResults(dbConnection, countQuery)[0]
    if(numOfResultsAtTheStart != numOfResultsAtTheEnd):
        return 0
    elif(numOfResultsAtTheStart == numOfResultsAtTheEnd):
        return 1

def testGetEmployeeID(dbConnection, employeeID):
    employeeQuery = f"SELECT * FROM Employee Where Employee_ID = {employeeID};"
    employeeIDs = getQueryResults(dbConnection, employeeQuery)
    if(len(employeeIDs) == 1):
        return(employeeIDs[0])
    else:
        return(None)
    
def testGetParkingSpotID(dbConnection, parkingSpotID):
    parkingSpotQuery = f"SELECT * FROM CustomerParkingSpot Where Parking_Spot_ID = {parkingSpotID};"
    parkingSpotIDs = getQueryResults(dbConnection, parkingSpotQuery)
    if(len(parkingSpotIDs) == 1):
        return(parkingSpotIDs[0])
    else:
        return(None)
    
def testEmployeeInsertion(dbConnection, employeeID, hireDate, terminationDate, title, employmentType, salary, 
          supervisor, addressLine1, addressLine2, postcode, city, birthDate, parkingSpotFK, vehicleFK, departmentFK, manageDepartment):
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
        return 1, "Employee successfully inserted"
    elif(getEmployee == employeeID and tryInsertingEmployee[0] == 1): # If returned employeeID matches with inserted ID and execute_query returns 1 - employee already exists
        return 2, "Failed to insert employee, there is already an employee with this ID"
    elif(getEmployee == None and tryInsertingEmployee[0] == 2):
        return 3, "Failed to insert employee, one of the attributes is in wrong type", f"Incorrect value: {tryInsertingEmployee[1]}"
    elif(getEmployee == employeeID and tryInsertingEmployee[0] == 2):
        return 4, "Failed to insert employee, one of the attributes is in wrong type and there is already an employee with this ID", f"Incorrect value: {tryInsertingEmployee[1]}"
    else:
        print("Unknown error, read the error message:")
        print(tryInsertingEmployee[1])
        return 0
        
def testCustomerParkingInsertion(dbConnection, parkingSpotID, parkingType, pricePerHour):
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
    
#===============================================================
# Main test
#===============================================================

def mainTest():
    print("===============================================================")
    print("Starting unit testing")
    print("===============================================================")
    numberOfPasses = 0
    numberOfFails = 0
    connection, _ , _ = create_server_connection("localhost","30330", "my_user", "my_password")
    
    # Test1: 
    #       Task: check connection to mariadb-galera-0 with valid credentials
    #       Expected result: 0 - connection should be successful
    test1 = create_server_connection("localhost","30330", "my_user", "my_password")
    if(test1[1] == None):
        print("✅ Test 1 pass: Connection to mariadb-galera-0 was established")
        numberOfPasses += 1
    else:
        print("❌ Test 1 fail: Connection could not be made to  mariadb-galera-0")
        numberOfFails += 1
        
    # Test1: 
    #       Task: check connection to mariadb-galera-1 with valid credentials
    #       Expected result: 0 - connection should be successful
    test2 = create_server_connection("localhost","30331", "my_user", "my_password")
    if(test2[1] == None):
        print("✅ Test 2 pass: Connection to mariadb-galera-1 was established")
        numberOfPasses += 1
    else:
        print("❌ Test 2 fail: Connection could not be made to  mariadb-galera-1")
        numberOfFails += 1
        
    # Test3: 
    #       Task: check connection to mariadb-galera-2 with valid credentials
    #       Expected result: 0 - connection should be successful
    test3 = create_server_connection("localhost","30332", "my_user", "my_password")
    if(test3[1] == None):
        print("✅ Test 3 pass: Connection to mariadb-galera-2 was established")
        numberOfPasses += 1
    else:
        print("❌ Test 3 fail: Connection could not be made to  mariadb-galera-2")
        numberOfFails += 1
        
    # Test4: 
    #       Task: check connection to mariadb-galera-3 with valid credentials
    #       Expected result: 0 - connection should be successful
    test4 = create_server_connection("localhost","30333", "my_user", "my_password")
    if(test4[1] == None):
        print("✅ Test 4 pass: Connection to mariadb-galera-3 was established")
        numberOfPasses += 1
    else:
        print("❌ Test 4 fail: Connection could not be made to  mariadb-galera-3")
        numberOfFails += 1
        
    # Test5: 
    #       Task: check connection to unknown db with valid credentials
    #       Expected result: 1 - connection should not be successful
    test5 = create_server_connection("localhost","30336", "my_user", "my_password")
    if(test5[1] == 1):
        print("✅ Test 5 pass: Connection to unknown db was not established")
        numberOfPasses += 1
    else:
        print(test5[2])
        print("❌ Test 5 fail: Connection could be made to unknown db")
        numberOfFails += 1
    
    # Test6: 
    #       Task: check connection to mariadb-galera-0 with invalid ip (not localhost)
    #       Expected result: 1 - connection should not be successful
    test6 = create_server_connection("not_localhost","30330", "my_user", "my_password")
    if(test6[1] == 1):
        print("✅ Test 6 pass: Connection to mariadb-galera-0 with invalid ip (not localhost) was not possible")
        numberOfPasses += 1
    else:
        print("❌ Test 6 fail: Connection to mariadb-galera-0 with invalid ip was possible")
        numberOfFails += 1
        
    # Test7: 
    #       Task: check connection to mariadb-galera-0 with invalid valid user
    #       Expected result: 2 - connection should not be successful
    test7 = create_server_connection("localhost","30330", "not_my_user", "my_password")
    if(test7[1] == 2):
        print("✅ Test 7 pass: Connection to mariadb-galera-0 with invalid user was not possible")
        numberOfPasses += 1
    else:
        print("❌ Test 7 fail: Connection to mariadb-galera-0 with invalid user was possible")
        numberOfFails += 1
    
    # Test8: 
    #       Task: check connection to mariadb-galera-0 with invalid valid password
    #       Expected result: 0 - connection should not be successful
    test8 = create_server_connection("localhost","30330", "my_user", "not_my_password")
    if(test8[1] == 2):
        print("✅ Test 8 pass: Connection to mariadb-galera-0 with invalid password was not possible")
        numberOfPasses += 1
    else:
        print("❌ Test 8 fail: Connection to mariadb-galera-0 with invalid password was possible")
        numberOfFails += 1
    
    # Test9: 
    #       Task: try removing employees
    #       Expected result: 0 - employee 999999999 shouldn't be found
    test9 = testRemoveEmployee(connection, 999999999)
    if(test9 == 1):
        print("✅ Test 9 pass: No employee was removed")
        numberOfPasses += 1
    else:
        print("❌ Test 9 fail: Employee was removed")
        numberOfFails += 1
    
    # Test10: 
    #       Task: get Employee data that matches 99999 from the DB
    #       Expected result: None - there shouldn't be an employee with this ID
    test10 = testGetEmployeeID(connection, 999999999)
    if(test10 == None):
        print("✅ Test 10 pass: No employee was not found")
        numberOfPasses += 1
    else:
        print("❌ Test 10 fail: Employee was found")
        numberOfFails += 1
        
    # Test11: 
    #       Task: generate an employee
    #       Expected result: 1 - employee should be created   
    test11 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999999, hireDate = "2022-12-13", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test11[0] == 1):
        print(f"✅ Test 11 pass: {test11[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 11 fail")
        numberOfFails += 1
          
    # Test12: 
    #       Task: fail to generate an employee based on duplicate ID
    #       Expected result: 2 - employee should be created   
    test12 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999999, hireDate = "2022-12-13", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test12[0] == 2):
        print(f"✅ Test 12 pass: {test12[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 12 fail")
        numberOfFails += 1
        
    # Test13: 
    #       Task: fail to generate an employee based on wrong attribute - hireDate
    #       Expected result: 3 - employee should be created   
    test13 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999998, hireDate = "hireDate", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test13[0] == 3):
        print(f"✅ Test 13 pass: {test13[1]} {test13[2]}")
        numberOfPasses += 1
    else:
        print("❌ Test 13 fail")
        numberOfFails += 1
        
    # Test14: 
    #       Task: fail to generate an employee based on duplicate ID and wrong attribute - hireDate
    #       Expected result: 4 - employee should be created   
    test14 = testEmployeeInsertion(dbConnection = connection, employeeID = 999999999, hireDate = "hireDate", terminationDate = "2022-12-14", title = "Test_Title", employmentType = "Test_Employment", salary = 9000, supervisor = 5, addressLine1 = "Test_Address_Line_1", addressLine2 = "Test_Address_Line_2", postcode = "Test_Postcode", city = "Test_City", birthDate = "2022-11-14", parkingSpotFK = 17, vehicleFK = 21, departmentFK = 5, manageDepartment = "null")
    if(test14[0] == 4):
        print(f"✅ Test 14 pass: {test14[1]} {test14[2]}")
        numberOfPasses += 1
    else:
        print("❌ Test 14 fail")
        numberOfFails += 1
        
    # Test15: 
    #       Task: remove employee generated from above
    #       Expected result: 1 - employee 999999999 shall be removed   
    test15 = testRemoveEmployee(dbConnection = connection, employeeID = 999999999)
    if(test15 == 0):
        print("✅ Test 15 pass: Employee was removed")
        numberOfPasses += 1
    else:
        print("❌ Test 15 fail: No employee was removed")
        numberOfFails += 1
        
    # Test16: 
    #       Task: generate a parking spot
    #       Expected result: 1 - parking spot should be created   
    test16 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6")
    if(test16[0] == 1):
        print(f"✅ Test 16 pass: {test16[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 16 fail")
        numberOfFails += 1
    
    # Test17: 
    #       Task: fail to generate a customer parking spot based on duplicate ID
    #       Expected result: 2 - there shouldn't be an customer parking spot with this ID
    test17 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6")
    if(test17[0] == 2):
        print(f"✅ Test 17 pass: {test17[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 17 fail")
        numberOfFails += 1
        
    # Test18: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 3 - under the limits
    #       Expected result: 3 - customer parking spot shouldn't be inserted due to constraints
    test18 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999997, parkingType = '{"1":" Car Parking "}' , pricePerHour = "3")
    if(test18[0] == 3):
        print(f"✅ Test 18 pass: {test18[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 18 fail")
        numberOfFails += 1
        
    # Test19: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 3 - under the limits and ID of 999999999 is taken
    #       Expected result: 4 - customer parking spot shouldn't be inserted due to constraints and ID
    test19 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "3")
    if(test19[0] == 4):
        print(f"✅ Test 19 pass: {test19[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 19 fail")
        numberOfFails += 1
        
    # Test20: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 400 - over the limits
    #       Expected result: 3 - customer parking spot shouldn't be inserted due to constraints  
    test20 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999997, parkingType = '{"1":" Car Parking "}' , pricePerHour = "400")
    if(test20[0] == 3):
        print(f"✅ Test 20 pass: {test20[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 20 fail")
        numberOfFails += 1
        
    # Test21: 
    #       Task: fail to generate a customer parking spot based on pricePerHour being 400 - over the limits
    #       Expected result: 4 - customer parking spot shouldn't be inserted due to constraints
    test21 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "400")
    if(test21[0] == 4):
        print(f"✅ Test 21 pass: {test21[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 21 fail")
        numberOfFails += 1
        
    # Test22: 
    #       Task: fail to generate a customer parking spot based on 6a being wrong type
    #       Expected result: 5 - failed to generate parking spot based on wrong type
    test22 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999997, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6a")
    if(test22[0] == 5):
        print(f"✅ Test 22 pass: {test22[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 22 fail")
        numberOfFails += 1
        
    # Test23: 
    #       Task: fail to generate a customer parking spot based on 6a being wrong type and same ID
    #       Expected result: 6 - failed to generate parking spot based on wrong type and same ID
    test23 = testCustomerParkingInsertion(dbConnection = connection, parkingSpotID = 999999999, parkingType = '{"1":" Car Parking "}' , pricePerHour = "6a")
    if(test23[0] == 6):
        print(f"✅ Test 23 pass: {test23[1]}")
        numberOfPasses += 1
    else:
        print("❌ Test 23 fail")
        numberOfFails += 1
        
        
    print("===============================================================")
    print("Unit testing has finished")
    print(f"Number of tests executed: {numberOfPasses + numberOfFails}")
    print(f"Number of passes: {numberOfPasses}")
    print(f"Number of fails: {numberOfFails}")
    print("===============================================================")
            
#===============================================================
# Run unit tests 1 - 23
#===============================================================

mainTest()
