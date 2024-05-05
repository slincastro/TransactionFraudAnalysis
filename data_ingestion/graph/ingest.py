from pymongo import MongoClient
from neo4j import GraphDatabase
import yaml

with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

uri = config['neo4j']['uri']
username = config['neo4j']['username']
password = config['neo4j']['password']
mongo_client_uri = config['mongodb']['client_uri']
db_name = config['mongodb']['db_name']
collection_name = config['mongodb']['collection_name']

def get_mongodb_collection():
    client = MongoClient(mongo_client_uri)
    db = client[db_name]
    return db[collection_name]

def get_neo4j_session():
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver.session()

def read_data_from_mongodb(collection):
    return list(collection.find({}))

def insert_data_into_neo4j(session, data):
    for item in data:
        session.run("""
        MERGE (u:Usuario {id_usuario: $Usuario.id_usuario})
        ON CREATE SET u.nombre = $Usuario.nombre, u.direccion = $Usuario.direccion, u.telefono = $Usuario.telefono, u.email = $Usuario.email

        MERGE (t:Transaccion {id_transaccion: $Transaccion.id_transaccion})
        ON CREATE SET t.monto = $Transaccion.monto, t.fecha_hora = $Transaccion.fecha_hora, t.tipo_transaccion = $Transaccion.tipo_transaccion, 
                        t.ubicacion = $Transaccion.ubicacion, t.dispositivo_usado = $Transaccion.dispositivo_usado, t.cuenta_destino = $Transaccion.cuenta_destino

        MERGE (c1:Cuenta {id_cuenta: $Cuenta.id_cuenta})
        ON CREATE SET c1.tipo_cuenta = $Cuenta.tipo_cuenta, c1.fecha_creacion = $Cuenta.fecha_creacion

        MERGE (c2:Cuenta {id_cuenta: $Transaccion.cuenta_destino})

        MERGE (d:Dispositivo {id_dispositivo: $Dispositivo.id_dispositivo})
        ON CREATE SET d.tipo_dispositivo = $Dispositivo.tipo_dispositivo, d.ubicacion_registrada = $Dispositivo.ubicacion_registrada

        MERGE (l:Ubicacion {ciudad: $Ubicacion.ciudad})
        ON CREATE SET l.pais = $Ubicacion.pais, l.coordenadas = $Ubicacion.coordenadas

        // Crear relaciones
        MERGE (u)-[:REALIZA]->(t)
        MERGE (t)-[:DESDE_CUENTA]->(c1)
        MERGE (t)-[:A_CUENTA]->(c2)
        MERGE (u)-[:POSEE]->(c1)
        MERGE (t)-[:UTILIZA]->(d)
        MERGE (t)-[:EJECUTADA_EN]->(l)
        MERGE (u)-[:MEDIANTE]->(d)
        """, {
            "Usuario": item['Usuario'],
            "Transaccion": item['Transaccion'],
            "Cuenta": item['Cuenta'],
            "Dispositivo": item['Dispositivo'],
            "Ubicacion": item['Ubicacion']
        })


def main():
    mongo_collection = get_mongodb_collection()

    data = read_data_from_mongodb(mongo_collection)

    with get_neo4j_session() as neo4j_session:
        insert_data_into_neo4j(neo4j_session, data)
        print("Datos insertados en Neo4j con éxito")

if __name__ == "__main__":
    main()
    

