from pymongo import MongoClient


client = MongoClient('mongodb://admin:password@localhost:27017/')


db = client['transactions']

collection = db['transaction_collection']

result = collection.delete_many({})


print(f'Documentos eliminados: {result.deleted_count}')
