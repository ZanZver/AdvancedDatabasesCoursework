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
no_runways = 10
no_airlines = 50
no_flights= 1500
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
driving_cats= ["A","B","C","D", "H","M"]
parking_types = ["Car Parking", "Motor Parking", "Handicap Parking"] 
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

def get_ids(connection, IDquery):
    execute_query(connection, "USE Airport_DB;")
    cursor = connection.cursor()
    try:
        cursor.execute(IDquery)
        table = cursor.fetchall()
        return([x[0] for x in table])
    except Error as err:
        print(f"Error: '{err}'")
        print(f"Query: '{IDquery}'")
        
def generate_supervisor(dbConnection):
    employee_query = "SELECT Employee_ID FROM Employee;"
    employee_ids = get_ids(dbConnection, employee_query)
    if(len(employee_ids) != 0):
        return random.choice(employee_ids)
    else:
        return 'null'

def get_data(entry):
    output = (str(tuple(entry.keys())).replace("'",""), str(tuple(entry.values())))
    return output if output[0][-2]!= "," else (output[0][:-2]+output[0][-1],output[1][:-2]+output[1][-1])

#puts the dummy data into the database
def populate(connection, lst, target):
    for entry in lst:
        columns,values= get_data(entry)
        query = ("INSERT INTO "+ target+ " "+ columns+ " VALUES "+ values).replace("'null'","null")
        execute_query(connection, query)

#===============================================================
# Dummy data generation for every table
#===============================================================
def generate_airlines(dbConnection):
    airlines = [{
        "Company_Name":fake.airline(),
        "Revenue":random.uniform(10000,100000)
        } for x in range(no_airlines)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, airlines, "Airline")
        
    print("===============================================================")
    print("Airline table finished")
    print("===============================================================")
    
def generate_certificates(dbConnection):
    employee_query = "SELECT Employee_ID FROM Employee;"
    qualification_query = "SELECT Qualification_ID FROM Qualification;"
    employee_ids = get_ids(dbConnection, employee_query)
    qualification_ids = get_ids(dbConnection, qualification_query)
    
    certificates = [{
        "Employee_FK":random.choice(employee_ids),
        "Certificate_Name":fake.sentence(5),
        "Achievement_Level":fake.sentence(3),
        "Qualification_FK": random.choice(qualification_ids)
        }for x in range(no_certs)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, certificates, "Certificate")
        
    print("===============================================================")
    print("Certificates table finished")
    print("===============================================================")
    
def generate_company_vehicles(dbConnection):
    department_query = "SELECT Department_ID FROM Department;"
    department_ids = get_ids(dbConnection, department_query)
    vehicles =[{
        "Vehicle_Name":fake.machine_year_make_model(),
        "Vehicle_Driving_License_Requirement":random.choice(driving_cats),
        "Department_FK":random.choice(department_ids)
        } for x in range(no_vehicles)
    ]
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,vehicles,"CompanyVehicle")
        
    print("===============================================================")
    print("CompanyVehicle table finished")
    print("===============================================================")
    
def generate_customers(dbConnection):
    parking_spot_query = "SELECT Parking_Spot_ID FROM CustomerParkingSpot;"
    parking_spot_ids = get_ids(dbConnection, parking_spot_query)
    customers = [{
        "Express_Lane":0 if (random.randrange(1,10)<9) else 1, #90% chance to not have express lane
        "Token_FK":random.choice(parking_spot_ids)
        } for x in range(no_customers)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, customers,"Customer")
        
    print("===============================================================")
    print("Customer table finished")
    print("===============================================================")
    
def generate_customer_parking_spots(dbConnection):     
    stri=[]
    for x in range(no_customer_parking_spots):
        stri.append("{")
        parking_spot = random.sample(parking_types,random.randrange(1,4))
        for y in range(len(parking_spot)):
            stri[x]+= '"'+str(y+1)+'":"'+parking_spot[y]+'", '
        stri[x] = stri[x][:-2]+"}"
        
    customer_parking_spots =[{
        "Parking_Type": stri[x],
        "Price_Per_Hour":random.randrange(5,300)
        }for x in range(no_customer_parking_spots)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,customer_parking_spots ,"CustomerParkingSpot")
        
    print("===============================================================")
    print("CustomerParkingSpot table finished")
    print("===============================================================")
    
def generate_departments(dbConnection):
    departments =[{
        "Department_Name":department_names[x],
        "Department_Location":fake.street_name()
        } for x in range(len(department_names))]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, departments,"Department")
        
    print("===============================================================")
    print("Department table finished")
    print("===============================================================")
        
def generate_employees(dbConnection):
    employee_parking_spot_query = "SELECT Parking_Spot_ID  FROM EmployeeParkingSpot;"
    company_vehicle_query = "SELECT Vehicle_ID FROM CompanyVehicle;"
    department_query = "SELECT Department_ID FROM Department;"
    employee_parking_spot_ids = get_ids(dbConnection, employee_parking_spot_query)
    company_vehicle_ids = get_ids(dbConnection, company_vehicle_query)
    department_ids = get_ids(dbConnection, department_query)
    
    for x in range(no_employees):
        employees =[{
                "Hire_Date":str(fake.date_this_decade()),
                "Termination_Date":str(fake.date_this_decade()) if (random.randrange(1,10)<2) else "null", #20% turnover,
                "Title": fake.job(),
                "Employment_Type":random.choice(employment_types),
                "Salary":random.uniform(3000,100000),
                "Supervisor":generate_supervisor(dbConnection),
                "Address_Line_1":fake.street_name(),
                "Address_Line_2":fake.building_number(),
                "Postcode": fake.postcode(),
                "City": fake.city(),
                "Birth_Date":str(fake.date_this_century()),
                "Parking_Spot_FK":random.choice(employee_parking_spot_ids),
                "Vehicle_FK":random.choice(company_vehicle_ids),
                "Department_FK":random.choice(department_ids),
                "Manage_Department":random.choice(department_ids)
            }]
        
        execute_query(dbConnection, "USE Airport_DB;")
        populate(dbConnection,employees,"Employee")
        
    print("===============================================================")
    print("Employee table finished")
    print("===============================================================")
   
def generate_employee_parking(dbConnection):   
    parking_types = ["Car Parking", "Motor Parking", "Handicap Parking"]       
    strii=[]
    for x in range(no_employee_parking_spots):
        strii.append("{")
        parking_spot = random.sample(parking_types,random.randrange(1,4))
        for y in range(len(parking_spot)):
            strii[x]+= '"'+str(y+1)+'":"'+parking_spot[y]+'", '
        strii[x] = strii[x][:-2]+"}"
 
    employee_parking_spots =[{
            "Parking_Type": strii[x]
        }for x in range(no_employee_parking_spots)]   
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,employee_parking_spots ,"EmployeeParkingSpot")
        
    print("===============================================================")
    print("EmployeeParking table finished")
    print("===============================================================")
 
def generate_flight(dbConnection):
    runwayQuery = "SELECT Runway_ID FROM Runway;"
    airlineQuery = "SELECT Company_ID FROM Airline;"
    runwayIDs = get_ids(dbConnection, runwayQuery)
    airlineIDs = get_ids(dbConnection, airlineQuery)
    
    flights = [{
        "Plane_Model":''.join(random.choice(string.ascii_uppercase) for _ in range(5)),
        "Departure_Time":str(fake.date_time_this_decade()),
        "Destination":fake.city(),
        "Gate":random.randrange(10,30),
        "Runway_FK":random.choice(runwayIDs),
        "Airline_FK":random.choice(airlineIDs),
        } for x in range(no_flights)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, flights, "Flight")
    
def generate_parking_tokens(dbConnection):
    parkingSpotQuery = "SELECT Parking_Spot_ID FROM CustomerParkingSpot;"
    parkingSpotIDs = get_ids(dbConnection, parkingSpotQuery)
    parking_tokens = [{
        "Date":str(fake.date_time_this_month()),
        "Parking_Spot_FK":random.choice(parkingSpotIDs),
        } for x in range(no_tokens)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, parking_tokens,"ParkingToken")
        
    print("===============================================================")
    print("ParkingToken table finished")
    print("===============================================================")
    
def generate_qualification(dbConnection):
    qualifications = [{
        "Qualification_Type":fake.sentence(5),
        "Qualification_Name":fake.sentence(5)
        } for x in range(no_qualifs)]

    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, qualifications, "Qualification")
        
    print("===============================================================")
    print("Qualification table finished")
    print("===============================================================")

def generate_runway(dbConnection):
    runways = [{
        "Length":random.uniform(2000,4000),
        "Width":random.uniform(8,80)
        } for x in range(no_runways)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, runways, "Runway")
        
    print("===============================================================")
    print("Runway table finished")
    print("===============================================================")

def generate_ticket(dbConnection):
    customer_query = "SELECT Customer_ID FROM Customer;"
    flight_query = "SELECT Flight_ID FROM Flight;"
    customer_ids = get_ids(dbConnection, customer_query)
    flight_ids = get_ids(dbConnection, flight_query)
    tickets = [{
        "Customer_FK":random.choice(customer_ids),
        "Flight_FK":random.choice(flight_ids)
        } for x in range(no_tickets)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, tickets,"Ticket")
        
    print("===============================================================")
    print("Ticket table finished")
    print("===============================================================")

def generate_employee_names(dbConnection):
    employee_query = "SELECT Employee_ID FROM Employee;"
    employee_ids = get_ids(dbConnection, employee_query)

    names = [{
        "Person_ID":employee_ids[x],
        "First_Name":fake.first_name(),
        "Middle_Name":fake.first_name() if (random.randrange(1,10)<8) else "null", #some people do not have a middle name. chance: 20%
        "Last_Name":fake.last_name(),
        "Is_Employee": 1
        }for x in range(len(employee_ids))]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(connection, names, "Name") 
        
    print("===============================================================")
    print("Name table - employees finished")
    print("===============================================================")
    
def generate_customer_names(dbConnection):
    customer_query = "SELECT Customer_ID FROM Customer;"
    customer_ids = get_ids(dbConnection, customer_query)

    names = [{
        "Person_ID":customer_ids[x],
        "First_Name":fake.first_name(),
        "Middle_Name":fake.first_name() if (random.randrange(1,10)<8) else "null", #some people do not have a middle name. chance: 20%
        "Last_Name":fake.last_name(),
        "Is_Employee": 0
        }for x in range(len(customer_ids))]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(connection, names, "Name") 
    
    print("===============================================================")
    print("Name table - customers finished")
    print("===============================================================")
    
#===============================================================
# Insert dummy data
#===============================================================

connection = create_server_connection("localhost","30330", "my_user", "my_password")

generate_runway(connection)
generate_airlines(connection)
generate_flight(connection)
generate_qualification(connection)
generate_customer_parking_spots(connection)
generate_employee_parking(connection)
generate_parking_tokens(connection)
generate_customers(connection)
generate_ticket(connection)
generate_departments(connection)
generate_company_vehicles(connection)
generate_employees(connection)
generate_certificates(connection)
generate_employee_names(connection)
generate_customer_names(connection)