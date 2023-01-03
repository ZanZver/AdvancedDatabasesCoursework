print("===============================================================")
print("Generating fake data")
print("===============================================================")


#===============================================================
# Import external libraries
#===============================================================
from faker import Faker
from faker_airtravel import AirTravelProvider
from faker_vehicle import VehicleProvider
#pip install faker
#pip install faker_airtravel
#pip install faker_vehicle

import random
import string
import mysql.connector
from mysql.connector import Error

#===============================================================
# Define data 
#===============================================================
increment = 4
#autoincrement is set to 4 on my machine for some reason and I have no idea how to fix it. 
# if it works fine on your end just replace the value above with 1
start = 1 
no_runways = 10
no_airlines = 50
no_flights= 80
no_qualifs = 30
no_tickets = 80
no_customers = 2500
no_employees = 2000
no_customer_parking_spots= 900
no_employee_parking_spots= 70
no_tokens = 1500
no_tickets = 2000
no_vehicles = 80
no_certs = 50
department_names = ["Landside operations", "Airside operations", "Billing and invoicing", "Information management"]
employment_types = ["Full-time", "Part-time", "Casual", "Fixed term", "Contract", "Apprentice", "Trainee", "Commission", "Piece rate"]

#===============================================================
# Initialize faker
#===============================================================

fake = Faker()
fake.add_provider(AirTravelProvider)
fake.add_provider(VehicleProvider)

#===============================================================
# Functions
#===============================================================

def generate_id(start, increment,no):
    return random.randrange(0,no-1)*increment+start

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
    except Error as err:
        print(f"Error: '{err}'")
        print(f"Query: '{query}'")

def getIDs(connection, IDquery):
    execute_query(connection, "USE Airport_DB;")
    cursor = connection.cursor()
    try:
        cursor.execute(IDquery)
        table = cursor.fetchall()
        #print("Query successful")
        return([x[0] for x in table])
    except Error as err:
        print(f"Error: '{err}'")
        print(f"Query: '{IDquery}'")
        
def generateSupervisor(dbConnection):
    employeeQuery = "SELECT Employee_ID FROM Employee;"
    employeeIDs = getIDs(dbConnection, employeeQuery)
    if(len(employeeIDs) != 0):
        return random.choice(employeeIDs)
    else:
        return 'null'

#get column names and the values for the sql query. Might act funny when there is only one attribute,
# which is why we covered it as a special case.
def get_data(entry):
    output = (str(tuple(entry.keys())).replace("'",""), str(tuple(entry.values())))
    return output if output[0][-2]!= "," else (output[0][:-2]+output[0][-1],output[1][:-2]+output[1][-1])

#puts the dummy data into the database
def populate(connection, lst, target):
    for entry in lst:
        columns,values= get_data(entry)
        query = ("INSERT INTO "+ target+ " "+ columns+ " VALUES "+ values).replace("'null'","null")
        #print(query+"\n")
        execute_query(connection, query)
    #print("Populated " + target + "\n")


#===============================================================
# Dummy data generation for every table
#===============================================================
def generateAirlines(dbConnection):
    airlines = [
        {"Company_Name":fake.airline(),
        "Revenue":random.uniform(10000,100000)
        } for x in range(no_airlines)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, airlines, "Airline")
        
    print("===============================================================")
    print("Airline table finished")
    print("===============================================================")
    
def generateCertificates(dbConnection):
    employeeQuery = "SELECT Employee_ID FROM Employee;"
    qualificationQuery = "SELECT Qualification_ID FROM Qualification;"
    employeeIDs = getIDs(dbConnection, employeeQuery)
    qualificationIDs = getIDs(dbConnection, qualificationQuery)
    
    certificates = [
        {
        "Employee_FK":random.choice(employeeIDs),
        "Certificate_Name":fake.sentence(5),
        "Achievement_Level":fake.sentence(3),
        "Qualification_FK": random.choice(qualificationIDs)
        }for x in range(no_certs)]
    #certficates must be done by hand if we have time.  the name and the level don't really make sense. but it is good placeholder data
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, certificates, "Certificate")
        
    print("===============================================================")
    print("Certificates table finished")
    print("===============================================================")
    
def generateCompanyVehicles(dbConnection):
    driving_cats= ["A","B","C","D", "H","M"]
    departmentQuery = "SELECT Department_ID FROM Department;"
    departmentIDs = getIDs(dbConnection, departmentQuery)
    vehicles =[
        {"Vehicle_Name":fake.machine_year_make_model(),
        "Vehicle_Driving_License_Requirement":random.choice(driving_cats),
        "Department_FK":random.choice(departmentIDs)
        } for x in range(no_vehicles)
    ]
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,vehicles,"CompanyVehicle")
        
    print("===============================================================")
    print("CompanyVehicle table finished")
    print("===============================================================")
    
def generateCustomers(dbConnection):
    parkingSpotQuery = "SELECT Parking_Spot_ID FROM CustomerParkingSpot;"
    parkingSpotIDs = getIDs(dbConnection, parkingSpotQuery)
    customers =   [
        {"Express_Lane":0 if (random.randrange(1,10)<9) else 1, #90% chance to not have express lane
        "Token_FK":random.choice(parkingSpotIDs)
        } for x in range(no_customers)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, customers,"Customer")
        
    print("===============================================================")
    print("Customer table finished")
    print("===============================================================")
    
def generateCustomerParkingSpots(dbConnection):
    parking_types = ["Car Parking", "Motor Parking", "Handicap Parking"]      
    stri=[]
    for x in range(no_customer_parking_spots):
        stri.append("{")
        parking_spot = random.sample(parking_types,random.randrange(1,4))
        for y in range(len(parking_spot)):
            stri[x]+= '"'+str(y+1)+'":"'+parking_spot[y]+'", '
        stri[x] = stri[x][:-2]+"}"
        
    customer_parking_spots =[
        {"Parking_Type": stri[x],
        "Price_Per_Hour":random.randrange(5,300)
        }for x in range(no_customer_parking_spots)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,customer_parking_spots ,"CustomerParkingSpot")
        
    print("===============================================================")
    print("CustomerParkingSpot table finished")
    print("===============================================================")
    
def generateDepartments(dbConnection):
    departments =[
        {"Department_Name":department_names[x],
        "Department_Location":fake.street_name()
        } for x in range(len(department_names))]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, departments,"Department")
        
    print("===============================================================")
    print("Department table finished")
    print("===============================================================")
        
def generateEmployees(dbConnection):
    employeeParkingSpotQuery = "SELECT Parking_Spot_ID  FROM EmployeeParkingSpot;"
    companyVehicleQuery = "SELECT Vehicle_ID FROM CompanyVehicle;"
    departmentQuery = "SELECT Department_ID FROM Department;"
    employeeParkingSpotIDs = getIDs(dbConnection, employeeParkingSpotQuery)
    companyVehicleIDs = getIDs(dbConnection, companyVehicleQuery)
    departmentIDs = getIDs(dbConnection, departmentQuery)
    
    for x in range(no_employees):
        employees =[
            {
                "Hire_Date":str(fake.date_this_decade()),
                "Termination_Date":str(fake.date_this_decade()) if (random.randrange(1,10)<2) else "null", #20% turnover,
                "Title": fake.job(),
                "Employment_Type":random.choice(employment_types),
                "Salary":random.uniform(3000,100000),
                "Supervisor":generateSupervisor(dbConnection),
                "Address_Line_1":fake.street_name(),
                "Address_Line_2":fake.building_number(),
                "Postcode": fake.postcode(),
                "City": fake.city(),
                "Birth_Date":str(fake.date_this_century()),
                "Parking_Spot_FK":random.choice(employeeParkingSpotIDs),
                "Vehicle_FK":random.choice(companyVehicleIDs),
                "Department_FK":random.choice(departmentIDs),
                "Manage_Department":random.choice(departmentIDs)
            }
            ]
        
        execute_query(dbConnection, "USE Airport_DB;")
        populate(dbConnection,employees,"Employee")
        
    print("===============================================================")
    print("Employee table finished")
    print("===============================================================")
   
def generateEmployeeParking(dbConnection):   
    parking_types = ["Car Parking", "Motor Parking", "Handicap Parking"]       
    strii=[]
    for x in range(no_employee_parking_spots):
        strii.append("{")
        parking_spot = random.sample(parking_types,random.randrange(1,4))
        for y in range(len(parking_spot)):
            strii[x]+= '"'+str(y+1)+'":"'+parking_spot[y]+'", '
        strii[x] = strii[x][:-2]+"}"
 
    employee_parking_spots =[
        {"Parking_Type": strii[x]
        }for x in range(no_employee_parking_spots)]   
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,employee_parking_spots ,"EmployeeParkingSpot")
        
    print("===============================================================")
    print("EmployeeParking table finished")
    print("===============================================================")
 
def generateFlight(dbConnection):
    runwayQuery = "SELECT Runway_ID FROM Runway;"
    airlineQuery = "SELECT Company_ID FROM Airline;"
    runwayIDs = getIDs(dbConnection, runwayQuery)
    airlineIDs = getIDs(dbConnection, airlineQuery)
    
    flights = [
        {"Plane_Model":''.join(random.choice(string.ascii_uppercase) for _ in range(5)),
        "Departure_Time":str(fake.date_time_this_decade()),
        "Destination":fake.city(),
        "Gate":random.randrange(10,30),
        "Runway_FK":random.choice(runwayIDs),
        "Airline_FK":random.choice(airlineIDs),
        } for x in range(no_flights)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, flights, "Flight")
    
def generateParkingTokens(dbConnection):
    parkingSpotQuery = "SELECT Parking_Spot_ID FROM CustomerParkingSpot;"
    parkingSpotIDs = getIDs(dbConnection, parkingSpotQuery)
    parking_tokens = [
        {"Date":str(fake.date_time_this_month()),
        "Parking_Spot_FK":random.choice(parkingSpotIDs),
        } for x in range(no_tokens)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, parking_tokens,"ParkingToken")
        
    print("===============================================================")
    print("ParkingToken table finished")
    print("===============================================================")
    
def generateQualification(dbConnection):
    qualifications = [
        {"Qualification_Type":fake.sentence(5),
        "Qualification_Name":fake.sentence(5)
        } for x in range(no_qualifs)]
    #this sucks! might do it by hand
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, qualifications, "Qualification")
        
    print("===============================================================")
    print("Qualification table finished")
    print("===============================================================")

def generateRunway(dbConnection):
    runways = [ 
        {"Length":random.uniform(2000,4000),
        "Width":random.uniform(8,80)
        } for x in range(no_runways)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, runways, "Runway")
        
    print("===============================================================")
    print("Runway table finished")
    print("===============================================================")

def generateTicket(dbConnection):
    customerQuery = "SELECT Customer_ID FROM Customer;"
    flightQuery = "SELECT Flight_ID FROM Flight;"
    customerIDs = getIDs(dbConnection, customerQuery)
    flightIDs = getIDs(dbConnection, flightQuery)
    tickets = [
        {"Customer_FK":random.choice(customerIDs),
        "Flight_FK":random.choice(flightIDs)
        } for x in range(no_tickets)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, tickets,"Ticket")
        
    print("===============================================================")
    print("Ticket table finished")
    print("===============================================================")

def generateEmployeeNames(dbConnection):
    employeeQuery = "SELECT Employee_ID FROM Employee;"
    employeeIDs = getIDs(dbConnection, employeeQuery)

    names = [
        {
        "Person_ID":employeeIDs[x],
        "First_Name":fake.first_name(),
        "Middle_Name":fake.first_name() if (random.randrange(1,10)<8) else "null", #some people do not have a middle name. chance: 20%
        "Last_Name":fake.last_name(),
        "Is_Employee": 1
        }for x in range(len(employeeIDs))]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(connection, names, "Name") 
        
    print("===============================================================")
    print("Name table - employees finished")
    print("===============================================================")
    
def generateCustomerNames(dbConnection):
    customerQuery = "SELECT Customer_ID FROM Customer;"
    customerIDs = getIDs(dbConnection, customerQuery)

    names = [
        {
        "Person_ID":customerIDs[x],
        "First_Name":fake.first_name(),
        "Middle_Name":fake.first_name() if (random.randrange(1,10)<8) else "null", #some people do not have a middle name. chance: 20%
        "Last_Name":fake.last_name(),
        "Is_Employee": 0
        }for x in range(len(customerIDs))]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(connection, names, "Name") 
    
    print("===============================================================")
    print("Name table - customers finished")
    print("===============================================================")
    
#===============================================================
# Insert dummy data
#===============================================================

connection = create_server_connection("localhost","30330", "my_user", "my_password")

# 1) - 10 runways
generateRunway(connection)

# 2) - 50 airlines
generateAirlines(connection)

# 3) - OK
generateFlight(connection)

# 4) - OK
generateQualification(connection)

# 5) - OK
generateCustomerParkingSpots(connection)

# 6) - OK
generateEmployeeParking(connection)

# 7) - OK
generateParkingTokens(connection)

# 8) - OK
generateCustomers(connection)

# 9) - OK
generateTicket(connection)

# 10) - OK
generateDepartments(connection)

# 11) - OK
generateCompanyVehicles(connection)

# 12) - OK
generateEmployees(connection)

# 13) - OK
generateCertificates(connection)

# 14a) - OK
generateEmployeeNames(connection)
# 14b) - OK
generateCustomerNames(connection)