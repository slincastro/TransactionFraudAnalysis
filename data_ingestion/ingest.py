from pymongo import MongoClient
import json

def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def connect_to_mongodb(username, password, host='localhost', port=27017, db_name='transactions'):
    uri = f"mongodb://{username}:{password}@{host}:{port}/"
    client = MongoClient(uri)
    return client[db_name]

def insert_data(data, db):

    if isinstance(data, list): 
        db.transaction_collection.insert_many(data)
    else: 
        db.transaction_collection.insert_one(data)

def main():
    data = load_data('data.json')

    db = connect_to_mongodb('admin', 'password')

    insert_data(data, db)

    print("Datos insertados con éxito")

if __name__ == "__main__":
    main()
