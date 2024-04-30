from pymongo import MongoClient

def connect_to_mongodb(username, password, host='localhost', port=27017, db_name='mydatabase'):
    # Conexión a MongoDB
    uri = f"mongodb://{username}:{password}@{host}:{port}/"
    client = MongoClient(uri)
    return client[db_name]

def count_documents(db, collection_name):
    # Contar documentos en una colección específica
    return db[collection_name].count_documents({})

def main():
    # Conectar a MongoDB
    db = connect_to_mongodb('admin', 'password')

    # Nombre de la colección a consultar
    collection_name = 'my_collection'

    # Contar los documentos
    document_count = count_documents(db, collection_name)

    print(f"Hay {document_count} documentos en la colección '{collection_name}'.")

if __name__ == "__main__":
    main()
