
print("===============================================================")
print("Generating fake data")
print("===============================================================")


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

increment=4
#autoincrement is set to 4 on my machine for some reason and I have no idea how to fix it. 
# if it works fine on your end just replace the value above with 1


start =1 

#-----------------------------------
#| How much dummy data is generated|
#-----------------------------------
no_runways = 3
no_airlines = 3
no_flights= 3
no_qualifs = 3
no_tickets = 3
no_customers = 3
no_employees = 3
no_names =no_customers+no_employees # Fix this
no_customer_parking_spots= 3
no_employee_parking_spots= 3
no_tokens = 3
no_tickets = 3
no_vehicles = 3
no_certs = 3
department_names =["Landside operations", "Airside operations", "Billing and invoicing", "Information management"]
employment_types= ["Full-time", "Part-time", "Casual", "Fixed term", "Contract", "Apprentice", "Trainee", "Commission", "Piece rate"]
no_departments = len(department_names)



#Faker and friends.

fake = Faker()
fake.add_provider(AirTravelProvider)
fake.add_provider(VehicleProvider)

#generates numbers for FKs
def generate_id(start, increment,no):
    return random.randrange(0,no-1)*increment+start



#SQL Stuff
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
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")



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
        
        print(query+"\n")
        
        execute_query(connection, query)
    print("Populated " + target + "\n")


#DUMMY DATA GENERATION STARTS HERE

# ======
def generateAirlines(dbConnection):
    airlines = [
        {"Company_Name":fake.airline(),
        "Revenue":random.uniform(10000,100000)
        } for x in range(no_airlines)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, airlines, "Airline")
    
def generateCertificates(dbConnection):
    certificates = [
        {
        "Employee_FK":generate_id(start,increment,no_employees),
        "Certificate_Name":fake.sentence(5),
        "Achievement_Level":fake.sentence(3),
        "Qualification_FK": generate_id(start,increment,no_qualifs)
        }for x in range(no_certs)]
    #certficates must be done by hand if we have time.  the name and the level don't really make sense. but it is good placeholder data
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, certificates, "Certificate")
    
def generateCompanyVehicles(dbConnection):
    driving_cats= ["A","B","C","D", "H","M"]
    vehicles =[
        {"Vehicle_Name":fake.machine_year_make_model(),
        "Vehicle_Driving_License_Requirement":random.choice(driving_cats),
        "Department_FK":generate_id(start,increment,no_departments)
        } for x in range(no_vehicles)
    ]
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,vehicles,"CompanyVehicle")
    
def generateCustomers(dbConnection):
    customers =   [
        {"Express_Lane":0 if (random.randrange(1,10)<9) else 1, #90% chance to not have express lane
        "Token_FK":generate_id(start,increment, no_tokens) if (random.randrange(1,10)<5) else "null" #50% chance to use a parking token
        } for x in range(no_customers)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, customers,"Customer")
    
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
    
def generateDepartments(dbConnection):
    departments =[
        {"Department_Name":department_names[x],
        "Department_Location":fake.street_name()
        } for x in range(no_departments)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, departments,"Department")
        
def generateEmployees(dbConnection):
    employees =[
        {
            "Hire_Date":str(fake.date_this_decade()),
            "Termination_Date":str(fake.date_this_decade()) if (random.randrange(1,10)<2) else "null", #20% turnover,
            "Title": fake.job(),
            "Employment_Type":random.choice(employment_types),
            "Salary":random.uniform(3000,100000),
            "Supervisor":a if (a:=generate_id(start,increment,no_employees)<x*increment+1)else 1, #if the generated supervisor does not exist then we assign the CEO (employee 1) as supervisor
            "Address_Line_1":fake.street_name(),
            "Address_Line_2":fake.building_number(),
            "Postcode": fake.postcode(),
            "City": fake.city(),
            "Birth_Date":str(fake.date_this_century()),
            "Parking_Spot_FK":generate_id(start,increment,no_employee_parking_spots) if (random.randrange(1,10)<60) else "null", #60% use the employee parking
            "Vehicle_FK":generate_id(start,increment,no_vehicles) if (random.randrange(1,10)<3) else "null", #30% use company vehicles
            "Department_FK":generate_id(start,increment,no_departments),
            "Manage_Department":"null",
        }for x in range(no_employees)
        ]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection,employees,"Employee")
   
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
 
def generateFlight(dbConnection):
    flights = [
        {"Plane_Model":''.join(random.choice(string.ascii_uppercase) for _ in range(5)),
        "Departure_Time":str(fake.date_time_this_decade()),
        "Destination":fake.city(),
        "Gate":random.randrange(10,30),
        "Runway_FK":generate_id(start,increment, no_runways),
        "Airline_FK":generate_id(start,increment, no_airlines)
        } for x in range(no_flights)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, flights, "Flight")

def generateName(dbConnection):
    people = list(range(0,no_employees))+list(range(0,no_customers))
    names = [
        {
        "Person_ID":people[x]*increment+1,
        "First_Name":fake.first_name(),
        "Middle_Name":fake.first_name() if (random.randrange(1,10)<8) else "null", #some people do not have a middle name. chance: 20%
        "Last_Name":fake.last_name(),
        "Is_Employee": 0 if (x >= no_employees) else 1 
        }for x in range(no_names)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, names, "Name") 
    
def generateParkingTokens(dbConnection):
    parking_tokens = [
        {"Date":str(fake.date_time_this_month()),
        "Parking_Spot_FK":generate_id(start,increment, no_customer_parking_spots)
        } for x in range(no_tokens)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, parking_tokens,"ParkingToken")
    
def generateQualification(dbConnection):
    qualifications = [
        {"Qualification_Type":fake.sentence(5),
        "Qualification_Name":fake.sentence(5)
        } for x in range(no_qualifs)]
    #this sucks! might do it by hand
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, qualifications, "Qualification")

def generateRunway(dbConnection):
    runways = [ 
        {"Length":random.uniform(2000,4000),
        "Width":random.uniform(8,80)
        } for x in range(no_runways)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, runways, "Runway")

def generateTicket(dbConnection):
    tickets = [
        {"Customer_FK":generate_id(start,increment, no_customers),
        "Flight_FK":generate_id(start,increment, no_flights),
        } for x in range(no_tickets)]
    
    execute_query(dbConnection, "USE Airport_DB;")
    populate(dbConnection, tickets,"Ticket")
# ======

#dbConnection

connection = create_server_connection("localhost","30330", "my_user", "my_password")
#connect to server

# Works fine
# generateAirline(connection)


# 1) - OK
#generateRunway(connection)

# 2) - OK
#generateAirlines(connection)

# 3) - OK
#generateFlight(connection)

# 4) - OK
#generateQualification(connection)

# 5) - OK
#generateCustomerParkingSpots(connection)

# 6) - OK
#generateEmployeeParking(connection)

# 7) - OK
#generateParkingTokens(connection)

# 8) - OK
#generateCustomers(connection)

# 9) - OK
#generateTicket(connection)

# 10) - OK
#generateDepartments(connection)

# 11) - OK
#generateCompanyVehicles(connection)

# 12) - OK
#generateEmployees(connection)

# 13) - OK
#generateCertificates(connection)