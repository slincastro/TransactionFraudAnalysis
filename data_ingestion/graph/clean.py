from neo4j import GraphDatabase
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

uri = config['neo4j']['uri']
username = config['neo4j']['username']
password = config['neo4j']['password']

class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def execute_query(self, query):
        if self.__driver is not None:
            with self.__driver.session() as session:
                result = session.run(query)
                return result

conn = Neo4jConnection(uri, username, password)

delete_query = """
MATCH (n)
DETACH DELETE n
"""

# Ejecutar la consulta
result = conn.execute_query(delete_query)

# Cerrar la conexión
conn.close()

if result:
    print("Todos los nodos y relaciones han sido eliminados.")
else:
    print("No se ejecutó la eliminación o ya no había datos.")
