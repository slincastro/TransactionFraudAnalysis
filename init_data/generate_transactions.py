import json
import random
from faker import Faker
from datetime import datetime, timedelta
from geopy.distance import geodesic
import heapq 

fake = Faker()

cities = [
        ("Quito", "-0.1806532,-78.4678382"),
        ("Guayaquil", "-2.1709979,-79.9223592"),
        ("Cuenca", "-2.9001285,-79.0058965"),
        ("Ambato", "-1.24908,-78.61675"),
        ("Manta", "-0.9676533,-80.7089101"),
        ("Esmeraldas", "0.9636513,-79.6561136"),
        ("Loja", "-3.99313,-79.20422"),
        ("Machala", "-3.25811,-79.95589"),
        ("Portoviejo", "-1.05558,-80.45445"),
        ("Santo Domingo", "-0.25209,-79.17268"),
        ("Ibarra", "0.3391763,-78.1222336"),
        ("Quevedo", "-1.022512,-79.4604035"),
        ("Riobamba", "-1.6635508,-78.654646"),
        ("Milagro", "-2.1346495,-79.5873629"),
        ("Latacunga", "-0.9345704,-78.6157989"),
        ("La Libertad", "-2.231472,-80.9009673"),
        ("Babahoyo", "-1.801926,-79.5346451"),
        ("Otavalo", "0.2341765,-78.2661743"),
        ("Chone", "-0.6837542,-80.0936136"),
        ("El Carmen", "-0.2662036,-79.455487"),
        ("Azogues", "-2.739735,-78.846489"),
        ("Guaranda", "-1.6086139,-79.0005645"),
        ("Sucua", "-2.468191,-78.166504"),
        ("Puyo", "-1.492392,-78.0024135"),
        ("Nueva Loja", "0.084047,-76.8823242"),
        ("Samborondón", "-1.9628752,-79.7242159"),
        ("Macas", "-2.3095065,-78.1116327"),
        ("Tulcan", "0.8095047,-77.7173068"),
        ("Sangolquí", "-0.3126313,-78.4453967"),
        ("Pasaje", "-3.3343513,-79.8167435"),
        ("Santa Rosa", "-3.4517923,-79.9603016"),
        ("Rosa Zarate", "0.328231,-79.4743979"),
        ("Balzar", "-1.3663961,-79.9062692"),
        ("Huaquillas", "-3.4760833,-80.2321035"),
        ("Bahía de Caráquez", "-0.5937778,-80.4207213"),
        ("La Troncal", "-2.4194044,-79.3448473"),
        ("Jipijapa", "-1.333017,-80.580134"),
        ("Montecristi", "-1.045825,-80.657185"),
        ("Pelileo", "-1.32632,-78.54376"),
        ("Salinas", "-2.2251585,-80.958416"),
        ("Valencia", "-1.267940,-79.653203"),
        ("Zamora", "-4.069594,-78.957094"),
        ("Puerto Francisco de Orellana", "-0.462203,-76.993107"),
        ("Santa Elena", "-2.226890,-80.858732"),
        ("Santa Ana", "-1.222042,-80.385391"),
        ("Pujili", "-0.950764,-78.684171"),
        ("Montalvo", "-1.794189,-79.333222"),
        ("Pedro Carbo", "-1.819475,-80.237418"),
        ("San Miguel", "-1.699519,-78.97844"),
        ("El Triunfo", "-1.934482,-79.986672"),
        ("Yantzaza", "-3.82773,-78.759466"),
        ("Catamayo", "-3.983833,-79.354492"),
        ("Calceta", "-0.849184,-80.167083"),
        ("Cayambe", "0.050653,-78.155371"),
        ("Gualaceo", "-2.88566,-78.775955"),
        ("Naranjal", "-2.66998,-79.6213"),
        ("Alausi", "-2.19793,-78.846619"),
        ("Naranjito", "-2.215687,-79.466897"),
        ("Velasco Ibarra", "-1.045301,-79.638737")
    ]

devices = []

def find_nearest_cities(city_name, num_cities=3):
    target = None

    for city, coords in cities:
        if city == city_name:
            target = coords
            break
    
    if not target:
        return f"No data for city: {city_name}"

    distances = []
    target_coords = tuple(map(float, target.split(',')))
    
    for city, coords in cities:
        if city != city_name:
            city_coords = tuple(map(float, coords.split(',')))
            distance = geodesic(target_coords, city_coords).kilometers
            distances.append((distance, city))
    
    closest_cities = heapq.nsmallest(num_cities, distances)
    
    return random.choice(closest_cities)[1]

def generate_user_account_pairs(num_pairs):
    user_account_pairs = []
    for _ in range(num_pairs):
        user = {
            "id_usuario": "USR" + str(random.randint(10000, 99999)),
            "nombre": fake.name(),
            "direccion": fake.address(),
            "telefono": fake.phone_number(),
            "email": fake.email(),
            "ciudad": generate_location()["ciudad"],
            "dispositivo": generate_device()["id_dispositivo"]
        }
        account = {
            "id_cuenta": "AC" + str(random.randint(100000000, 999999999)),
            "tipo_cuenta": random.choice(["cuenta corriente", "cuenta de ahorros", "cuenta empresarial"]),
            "fecha_creacion": fake.date_between(start_date='-5y', end_date='today').isoformat()
        }
        user_account_pairs.append((user, account))
    return user_account_pairs

def generate_amount():

    if random.random() < 0.02:
        number = random.uniform(100000, 2000000)  
    else:
        number = random.uniform(100, 10000)
    
    return round(number, 2)

def generate_transaction(usuario, cuenta):
    tipos_transaccion = ["deposito", "retiro", "pago", "transferencia"]
    return {
        "id_transaccion": "TX" + str(random.randint(100000000, 999999999)),
        "monto": generate_amount(),
        "fecha_hora": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "tipo_transaccion": random.choice(tipos_transaccion),
        "ubicacion": find_nearest_cities(usuario["ciudad"]),
        "dispositivo_usado": usuario["dispositivo"],
        "cuenta_destino": cuenta["id_cuenta"]
    }

def generate_device():
    tipos_dispositivo = ["teléfono", "computadora", "tablet"]
    
    device = {
        "id_dispositivo": "DISP" + str(random.randint(1, 10000)),
        "tipo_dispositivo": random.choice(tipos_dispositivo)
    }
    devices.append(device)
    
    return device

def get_device_by_id(id):
    for dispositivo in devices:
        if dispositivo["id_dispositivo"] == id:
            return dispositivo
    return None


def generate_location():
    
    ciudad, coordenadas = random.choice(cities)

    return {
        "ciudad": ciudad,
        "pais": "Ecuador",
        "coordenadas": coordenadas
    }

def generate_records(num_records, user_account_pairs):
    data = []
    for _ in range(num_records):
        usuario, cuenta = random.choice(user_account_pairs)  
        record = {
            "Transaccion": generate_transaction(usuario, cuenta),
            "Cuenta": cuenta,
            "Usuario": usuario,
            "Dispositivo": get_device_by_id(usuario["dispositivo"]) ,
            "Ubicacion": generate_location()
        }
        data.append(record)
    return data


def get_records(num_records, num_users):
    user_account_pairs = generate_user_account_pairs(num_users)
    records = generate_records(num_records, user_account_pairs)
    return records

def main(records, filename='data.json'):   
    with open(filename, 'w') as f:
        json.dump(records, f, indent=4)
        
def get_total_inserted_rows():
    
    filename = 'data.json'
    
    try:
        with open(filename, 'r') as file:
            data = json.load(file) 
            record_count = len(data)
            print(f"Se encontraron {record_count} objetos")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError as error:
        print(f"Error: El contenido del archivo no es un JSON válido. {error}")
    except Exception as error:  
        print(f"Ocurrió un error inesperado: {error}")



if __name__ == "__main__":
    documents_to_insert = 1000  
    
    records = get_records(100,20)
    records.extend(get_records(100, 5))
    records.extend(get_records(1000, 10))
    records.extend(get_records(2000, 3))
    main(records)
    get_total_inserted_rows()


