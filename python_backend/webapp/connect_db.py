from pymongo import mongo_client
import os

def get_database():

    DB_USERNAME=str(os.getenv("DB_USERNAME"))
    DB_PASSWORD=str(os.getenv("DB_PASSWORD"))
    DB_CLUSTER_NAME=str(os.getenv("DB_CLUSTER_NAME"))
    DB_BASE_NAME=str(os.getenv("DB_BASE_NAME"))
    for var in (DB_BASE_NAME, DB_CLUSTER_NAME, DB_PASSWORD, DB_USERNAME):
        if not var: raise ValueError ("Variáveis de ambiente com credenciais de banco não inseridas")

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_CLUSTER_NAME}.mongodb.net/?retryWrites=true&w=majority"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = mongo_client.MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client[DB_BASE_NAME]

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    dbname = get_database()
    collection_name = dbname["notas"]
