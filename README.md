# Advanced Databases Coursework
Group project for Advanced Databases module.

## Table of Contents
- [Advanced Databases Coursework](#advanced-databases-coursework)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
    - [Team](#team)
    - [Software used](#software-used)
  - [Environment setup](#environment-setup)
  - [Structure](#structure)

## About
Goal of the project is to create highly available relational database that can store airports data.

### Team
- Daniel Rimaru
  - Student ID: 19134702
- Zan Zver
   - Student ID: 18133498
  
### Software used
- Docker - version 20.10.21, build baeda1f
    - used for vitalising databases
- MariaDB - version 10.9.3
    - used for storing data, in order to achieve high availability Galera cluster was added
- Python - version 3.9
    - used for creating data and testing database
- Dbever - version 22.3.1
    - user interface for connection to the database(s)

## Environment setup
Assuming that you have installed all of the software from above ([Software used](#software-used)), you follow instructions bellow in order to get this project up and running:
<ol>
  <li>
    Download the project
  </li>
  <li>
    Open Docker folder in terminal
  </li>
  <li>
    Create new network
    <pre><code>docker network create -d bridge galera-cluster-net</code></pre>
  </li>
  <li>
    Start up docker containers with <pre><code>docker-compose up -d</code></pre>
  </li>
  <li>
    Open Dbever (or any other program) and execute DDL.sql script
  </li>
  <li>
    Execute PROCEDURE.sql
  </li>
  <li>
    In Python, execute DummyData.py in order to insert data
  </li>
  <li>
    To test constraints, execute Testing.py in Python as well
  </li>
</ol>

Do note that steps 1-5 are required, while steps 6-8 are optional.


## Structure
Structure of the GitHub file tree.
```
DataMiningCoursework
│   README.md
│
└─── Code
│   └─── Docker
│       └─── DDL
│       │   └─── docker-compose.yml
│       │        Docker compose setup of the physical system
│   └─── SQL
│       └─── DDL
│       │   └─── Data Definition Language - creation of table(s)
│       │   │    DDL.sql
│       │   │    └─── DDL file
│       │   │    PROCEDURE.sql
│       │   │    └─── PROCEDURE file for GetParkingToBePaid procedure
│       └─── DML
│       │   └─── Data Manipulation Language - CRUD operation on table(s)
│       │   │    DummyData.py
│       │   │    └─── Script for inserting SQL code
│       │   │    Testing.py
│       │   │    └─── Script that tests database in unit testing style
│       │   │    Queries
│       │   │           └─── Daniel
│       │   │           │    Query1.SQL
│       │   │           │    └─── Individual Query1 code 
│       │   │           │    Query2.SQL
│       │   │           │    └─── Individual Query2 code 
│       │   │           │    Query3.SQL
│       │   │           │    └─── Individual Query2 code 
│       │   │           │    Optimization.SQL
│       │   │           │    └─── Code for individual optimization technique
│       │   │           └─── Zan
│       │   │           │    Query1.SQL
│       │   │           │    └─── Individual Query1 code 
│       │   │           │    Query2.SQL
│       │   │           │    └─── Individual Query2 code 
│       │   │           │    Query3.SQL
│       │   │           │    └─── Individual Query2 code 
│       │   │           │    Optimization.SQL
│       │   │           │    └─── Code for individual optimization technique
│   
└─── Documents
│    └─── Design
│        │    Design.png
│        │    └───   Physical design representation
```