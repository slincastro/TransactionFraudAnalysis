import json
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_transaction():
    tipos_transaccion = ["depósito", "retiro", "pago", "transferencia"]
    return {
        "id_transaccion": "TX" + str(random.randint(100000000, 999999999)),
        "monto": round(random.uniform(100, 10000), 2),
        "fecha_hora": (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
        "tipo_transaccion": random.choice(tipos_transaccion),
        "ubicacion": fake.city(),
        "dispositivo_usado": "DISP" + str(random.randint(1, 10000)),
        "cuenta_destino": "AC" + str(random.randint(100000000, 999999999))
    }

def generate_account():
    tipos_cuenta = ["cuenta corriente", "cuenta de ahorros", "cuenta empresarial"]
    return {
        "id_cuenta": "AC" + str(random.randint(100000000, 999999999)),
        "tipo_cuenta": random.choice(tipos_cuenta),
        "fecha_creacion": (datetime.now() - timedelta(days=random.randint(365, 365*5))).isoformat()
    }

def generate_user():
    return {
        "id_usuario": "USR" + str(random.randint(10000, 99999)),
        "nombre": fake.name(),
        "direccion": fake.address(),
        "telefono": fake.phone_number(),
        "email": fake.email()
    }

def generate_device():
    tipos_dispositivo = ["teléfono", "computadora", "tablet"]
    return {
        "id_dispositivo": "DISP" + str(random.randint(1, 10000)),
        "tipo_dispositivo": random.choice(tipos_dispositivo),
        "ubicacion_registrada": fake.city()
    }

def generate_location():
    return {
        "ciudad": fake.city(),
        "pais": fake.country(),
        "coordenadas": f"{fake.latitude()},{fake.longitude()}"
    }

def generate_records(num_records):
    data = []
    for _ in range(num_records):
        record = {
            "Transaccion": generate_transaction(),
            "Cuenta": generate_account(),
            "Usuario": generate_user(),
            "Dispositivo": generate_device(),
            "Ubicacion": generate_location()
        }
        data.append(record)
    return data

def main(num_records, filename='data.json'):
    records = generate_records(num_records)
    with open(filename, 'w') as f:
        json.dump(records, f, indent=4)

if __name__ == "__main__":
    documents_to_insert = 10
    main(documents_to_insert = 10)  
