from pymongo import MongoClient
import json

def load_data(file_path):
    # Cargar datos desde un archivo JSON
    with open(file_path, 'r') as file:
        return json.load(file)

def connect_to_mongodb(username, password, host='localhost', port=27017, db_name='mydatabase'):
    # Conexión a MongoDB
    uri = f"mongodb://{username}:{password}@{host}:{port}/"
    client = MongoClient(uri)
    return client[db_name]

def insert_data(data, db):
    # Insertar datos en MongoDB
    if isinstance(data, list):  # Si data es una lista de registros
        db.my_collection.insert_many(data)
    else:  # Si data es un solo documento
        db.my_collection.insert_one(data)

def main():
    # Carga de datos
    data = load_data('data.json')

    # Conectar a MongoDB
    db = connect_to_mongodb('admin', 'password')

    # Insertar datos
    insert_data(data, db)

    print("Datos insertados con éxito")

if __name__ == "__main__":
    main()
