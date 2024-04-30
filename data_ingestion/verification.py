from pymongo import MongoClient

def connect_to_mongodb(username, password, host='localhost', port=27017, db_name='transactions'):

    uri = f"mongodb://{username}:{password}@{host}:{port}/"
    client = MongoClient(uri)
    return client[db_name]

def count_documents(db, collection_name):

    return db[collection_name].count_documents({})

def main():
    db = connect_to_mongodb('admin', 'password')

    collection_name = 'transaction_collection'

    document_count = count_documents(db, collection_name)

    print(f"Hay {document_count} documentos en la colección '{collection_name}'.")

if __name__ == "__main__":
    main()
