from multiprocessing import connection
import pymysql.cursors
import sys

#A module that contains functions to manipulate a MySQL server.


#Used to connect to a server without any databases
#hostName: Name of the host computer
#userName: Name of the user of the server
#userPass: Password for the server
def serverConnection(hostName,userName,userPass):
    connection = None
    try:
        connection = pymysql.connect(
            host = hostName,
            user = userName,
            passwd = userPass
        )
        print("MySQL Database connection successful")

    except Exception as err:
        sys.exit(f"Error: '{err}'")
        connection = None
    
    return connection

#Used to create an empty database
#connection: The connection object that is connected to the server
#dbName: Database name to be given by the user
def dbCreation(connection,dbName):
    cursor = connection.cursor()
    query = "CREATE DATABASE " + dbName
    try:
        cursor.execute(query)
        print("Command: " + query)
        print("Database " + dbName + " created successfully")
    except Exception as err:
        print(f"Error: '{err}'")
        sys.exit(f"Error: '{err}'")

#Used to connect to an already existing database
#hostName: Name of the host computer
#userName: Name of the user of the server
#userPass: Password for the server
#dbName: Database name to be given by the user
def dbConnection(hostName,userName,userPass,dbName):
    connection = None
    try:
        connection = pymysql.connect(
            host = hostName,
            user = userName,
            passwd = userPass,
            database = dbName
        )

        print(dbName + " Database connection successful")
    except Exception as err:
        sys.exit(f"Error: '{err}'")
        connection = None
    
    return connection

#Used to execute any query set by the user
#connection: The connection object that is connected to the server
#query: Command to be executed 
def queryExecute(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as err:
        sys.exit(f"Error: '{err}'")

