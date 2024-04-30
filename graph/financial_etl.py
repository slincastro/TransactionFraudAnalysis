from pymongo import MongoClient
from neo4j import GraphDatabase

# Configuración de MongoDB
def get_mongodb_collection():
    client = MongoClient("mongodb://admin:password@localhost:27017/")
    db = client['mydatabase']
    return db['my_collection']

# Configuración de Neo4j
def get_neo4j_session():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    return driver.session()

# Leer datos de MongoDB
def read_data_from_mongodb(collection):
    return list(collection.find({}))

# Insertar datos en Neo4j
def insert_data_into_neo4j(session, data):
    for item in data:
        print(item)
        # Aquí puedes adaptar la consulta según la estructura de tus datos y cómo quieres modelarlos en Neo4j
        query = """
        CREATE (n:Node {id: $id, name: $name})
        """
        session.run(query, id=item['_id'], name=item['name'])

def main():
    # Conectarse a MongoDB
    mongo_collection = get_mongodb_collection()

    # Leer datos
    data = read_data_from_mongodb(mongo_collection)

    # Conectarse a Neo4j
    with get_neo4j_session() as neo4j_session:
        # Insertar datos
        insert_data_into_neo4j(neo4j_session, data)
        print("Datos insertados en Neo4j con éxito")

if __name__ == "__main__":
    main()
