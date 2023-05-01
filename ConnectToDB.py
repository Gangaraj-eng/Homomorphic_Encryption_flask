# This file creates the database 
# and return database object
import os
import pymongo
from dotenv import load_dotenv

# loading the environment variables
load_dotenv()


def get_user_collection():
    # getting connection string
    MYDB_Connection_String=os.environ.get("COSMOS_CONNECTION_STRING")

    DatabaseName="FHE_Project"
    UsersCollection="Users"

    # getting client 
    db_client=pymongo.MongoClient(MYDB_Connection_String)

    database=db_client[DatabaseName]

    user_collection=database[UsersCollection]

    print(f"Connection to the database : {database.name}")
          
    return user_collection
