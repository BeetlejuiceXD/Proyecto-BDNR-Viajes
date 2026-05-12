import csv
import json
import pydgraph
from datetime import datetime

# Este archivo toma los CSV y los mete a Mongo Cassandra y Dgraph.
DATA_DIR = "Data/"


def read_csv(name):
    # Leemos un CSV como lista de diccionarios para usar nombres de columnas.
    with open(DATA_DIR + name) as f:
        return list(csv.DictReader(f))


def to_date(value):
    # Convertimos texto de fecha a datetime para las bases de cassandra y mongodb.
    return datetime.strptime(value, "%Y-%m-%d")

#MONGODB

#Funcion de drop para borrar los datos de mongodb.
def drop_mongo(db):
    # Limpiamos las colecciones para cargar datos desde cero.
    db.packages.drop()
    db.reservations.drop()
    db.hotels.drop()
    db.itineraries.drop()
    db.flights.drop()
    print("  MongoDB: colecciones borradas")

#Funcion de los indices que se definieron en el doc.
def create_mongo_indexes(db):
    # Creamos los indices que se definieron en el doc.
    db.packages.create_index("destination_name")
    db.packages.create_index("package_id", unique=True)
    db.reservations.create_index([("user_id", 1), ("year", 1), ("booking_date", -1)])
    db.reservations.create_index([("season", 1), ("destination_name", 1)])
    db.reservations.create_index([("year", 1), ("destination_name", 1)])
    db.reservations.create_index("reservation_id", unique=True)
    db.hotels.create_index([("price_range", 1), ("rating", -1)])
    db.hotels.create_index("hotel_id", unique=True)
    db.itineraries.create_index("user_id")
    db.itineraries.create_index("itinerary_id", unique=True)
    db.flights.create_index("price")
    db.flights.create_index("id_flight", unique=True)
    print("  MongoDB: indices creados")


def load_mongo(db):
    drop_mongo(db)  # Evita la duplicacion al cargar varias veces

    # Paquetes turisticos que se consultan por destino.
    packages = []
    for row in read_csv("packages.csv"):
        packages.append({
            "package_id": row["package_id"],
            "destination_id": row["destination_id"],
            "destination_name": row["destination_name"],
            "location": row["location"],
            "hotel_id": row["hotel_id"],
            "hotel_name": row["hotel_name"],
            "airline_name": row["airline_name"],
            "final_price": float(row["final_price"]),
            "season": row["season"],
        })

    # Reservaciones con fechas y precios ya convertidos para agregaciones.
    reservations = []
    for row in read_csv("reservations.csv"):
        reservations.append({
            "reservation_id": row["reservation_id"],
            "user_id": row["user_id"],
            "user_name": row["user_name"],
            "destination_id": row["destination_id"],
            "destination_name": row["destination_name"],
            "hotel_id": row["hotel_id"],
            "hotel_name": row["hotel_name"],
            "id_flight": row["id_flight"],
            "airline": row["airline"],
            "booking_date": to_date(row["booking_date"]),
            "year": int(row["year"]),
            "season": row["season"],
            "price": float(row["price"]),
            "status": row["status"],
        })

    # Hoteles con rating precio y rango de precio.
    hotels = []
    for row in read_csv("hotels.csv"):
        hotels.append({
            "hotel_id": row["hotel_id"],
            "hotel_name": row["hotel_name"],
            "destination_id": row["destination_id"],
            "destination_name": row["destination_name"],
            "location": row["location"],
            "country": row["country"],
            "rating": float(row["rating"]),
            "price": float(row["price"]),
            "price_range": row["price_range"],
            "available_rooms": int(row["available_rooms"]),
        })

    # Itinerarios que pertenecen a cada usuario.
    itineraries = []
    for row in read_csv("itineraries.csv"):
        itineraries.append({
            "itinerary_id": row["itinerary_id"],
            "user_id": row["user_id"],
            "destination_id": row["destination_id"],
            "destination_name": row["destination_name"],
            "start_date": to_date(row["start_date"]),
            "end_date": to_date(row["end_date"]),
            "selected_flight": row["selected_flight"],
            "selected_hotel": row["selected_hotel"],
            "status": row["status"],
        })

    # Vuelos con fechas y lugares de salida.
    flights = []
    for row in read_csv("flights.csv"):
        flights.append({
            "id_flight": row["id_flight"],
            "airline": row["airline"],
            "origin": row["origin"],
            "destination_id": row["destination_id"],
            "destination_name": row["destination_name"],
            "departure_date": to_date(row["departure_date"]),
            "price": float(row["price"]),
            "available_seats": int(row["available_seats"]),
        })

    # Insertamos todo en Mongo y despues creamos indices.
    db.packages.insert_many(packages)
    db.reservations.insert_many(reservations)
    db.hotels.insert_many(hotels)
    db.itineraries.insert_many(itineraries)
    db.flights.insert_many(flights)
    create_mongo_indexes(db)
    print("  MongoDB: datos cargados")
#                    CASSANDRA


def drop_cassandra(session):
    # Borre  tablas de Cassandra para evitar datos repetidos.
    tables = [
        "reservaciones_lugar",
        "reservaciones_por_estado",
        "tarifas_hotel",
        "busquedas_usuario",
        "catalogo_actividades",
        "disponibilidad_hoteles",
        "actividades_reserva",
    ]
    for table in tables:
        session.execute("DROP TABLE IF EXISTS " + table)
    print("  Cassandra: tablas borradas")


def create_cassandra_schema(session):
    # Hice las tablas del doc con sus Pk y su Ck
    session.execute("CREATE TABLE IF NOT EXISTS reservaciones_lugar (user_id TEXT, destination_name TEXT, date DATE, reservation_id TEXT, cost FLOAT, PRIMARY KEY ((user_id, destination_name), date)) WITH CLUSTERING ORDER BY (date DESC)")
    session.execute("CREATE TABLE IF NOT EXISTS reservaciones_por_estado (user_id TEXT, status TEXT, reservation_time DATE, reservation_id TEXT, destination_name TEXT, hotel_name TEXT, id_flight TEXT, PRIMARY KEY ((user_id, status), reservation_time)) WITH CLUSTERING ORDER BY (reservation_time DESC)")
    session.execute("CREATE TABLE IF NOT EXISTS tarifas_hotel (hotel_name TEXT, date DATE, room_type TEXT, price FLOAT, PRIMARY KEY ((hotel_name), date, room_type))")
    session.execute("CREATE TABLE IF NOT EXISTS busquedas_usuario (user_id TEXT, search_time DATE, destination_name TEXT, departure_city TEXT, travelers_count INT, PRIMARY KEY ((user_id), search_time)) WITH CLUSTERING ORDER BY (search_time DESC)")
    session.execute("CREATE TABLE IF NOT EXISTS catalogo_actividades (destination_id TEXT, category TEXT, activity_name TEXT, price FLOAT, PRIMARY KEY ((destination_id), category, activity_name))")
    session.execute("CREATE TABLE IF NOT EXISTS disponibilidad_hoteles (destination_id TEXT, hotel_name TEXT, hotel_id TEXT, available_rooms INT, start_date DATE, end_date DATE, PRIMARY KEY ((destination_id), hotel_name))")
    session.execute("CREATE TABLE IF NOT EXISTS actividades_reserva (reservation_id TEXT, activity_name TEXT, category TEXT, PRIMARY KEY ((reservation_id), activity_name))")
    print("  Cassandra: tablas creadas")


def load_cassandra(session):
    # Cassandra se carga las tablas
    drop_cassandra(session)
    create_cassandra_schema(session)

    # Guarde reservaciones por lugar y tambien por estado.
    stmt1 = session.prepare("INSERT INTO reservaciones_lugar (user_id, destination_name, date, reservation_id, cost) VALUES (?, ?, ?, ?, ?)")
    stmt2 = session.prepare("INSERT INTO reservaciones_por_estado (user_id, status, reservation_time, reservation_id, destination_name, hotel_name, id_flight) VALUES (?, ?, ?, ?, ?, ?, ?)")
    for row in read_csv("reservations.csv"):
        fecha = to_date(row["booking_date"]).date()
        session.execute(stmt1, [row["user_id"], row["destination_name"], fecha, row["reservation_id"], float(row["price"])])
        session.execute(stmt2, [row["user_id"], row["status"], fecha, row["reservation_id"], row["destination_name"], row["hotel_name"], row["id_flight"]])
    print("  reservaciones ")

    # Guardamos tarifas de hotel por fecha y tipo de cuarto.
    stmt = session.prepare("INSERT INTO tarifas_hotel (hotel_name, date, room_type, price) VALUES (?, ?, ?, ?)")
    for row in read_csv("tarifas_hotel.csv"):
        session.execute(stmt, [row["hotel_name"], to_date(row["date"]).date(), row["room_type"], float(row["price"])])
    print("  tarifas ")

    # Guardamos busquedas para poder consultar por usuario y rango de fechas.
    stmt = session.prepare("INSERT INTO busquedas_usuario (user_id, search_time, destination_name, departure_city, travelers_count) VALUES (?, ?, ?, ?, ?)")
    for row in read_csv("searches.csv"):
        session.execute(stmt, [row["user_id"], to_date(row["search_date"]).date(), row["destination_name"], row["departure_city"], int(row["travelers_count"])])
    print("  busquedas ")

    # Guardamos actividades por destino y categoria.
    stmt = session.prepare("INSERT INTO catalogo_actividades (destination_id, category, activity_name, price) VALUES (?, ?, ?, ?)")
    for row in read_csv("activities.csv"):
        session.execute(stmt, [row["destination_id"], row["category"], row["activity_name"], float(row["price"])])
    print("  catalogo ")

    # Guardamos disponibilidad simple de hoteles por destino.
    stmt = session.prepare("INSERT INTO disponibilidad_hoteles (destination_id, hotel_name, hotel_id, available_rooms, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)")
    for row in read_csv("hotels.csv"):
        session.execute(stmt, [row["destination_id"], row["hotel_name"], row["hotel_id"], int(row["available_rooms"]), datetime(2026, 1, 1).date(), datetime(2026, 12, 31).date()])
    print("  disponibilidad")

    # Guardamos que actividades se hicieron en cada reserva.
    stmt = session.prepare("INSERT INTO actividades_reserva (reservation_id, activity_name, category) VALUES (?, ?, ?)")
    for row in read_csv("reservation_activities.csv"):
        session.execute(stmt, [row["reservation_id"], row["activity_name"], row["category"]])
    print("  Cassandra listo")

# =====================================================
#                    DGRAPH
# =====================================================
def drop_dgraph(client):
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)
    print("  Dgraph: todo borrado")
def create_dgraph_schema(client):
    schema = """
    user_id: string @index(hash) .
    user_name: string @index(hash) .
    email: string @index(hash) .

    destination_id: string @index(hash) .
    destination_name: string @index(hash) .
    location: string @index(hash) .
    price: float @index(float) .

    activity_id: string @index(hash) .
    activity_name: string @index(hash) .

    hotel_id: string @index(hash) .
    hotel_name: string @index(hash) .
    stars: int .

    category_name: string @index(hash) .
    name: string @index(hash) .
    code: string .

    amigo: [uid] .
    destino: [uid] @reverse @count .
    hizo_actividad: [uid] .
    category: uid @reverse .
    pais: uid @reverse .
    hospedaje: [uid] .
    tiene_actividad: [uid] .
    region: uid @reverse .

    type User {
        user_id
        user_name
        email
        amigo
        destino
        hizo_actividad
    }

    type Destination {
        destination_id
        destination_name
        price
        location
        category
        pais
        hospedaje
    }

    type Activity {
        activity_id
        activity_name
        price
    }

    type Hotel {
        hotel_id
        hotel_name
        stars
        price
        tiene_actividad
    }

    type Category {
        category_name
    }

    type Country {
        name
        code
        region
    }

    type Region {
        name
    }
    """
    op = pydgraph.Operation(schema=schema)
    client.alter(op)
    print("  Dgraph: esquema creado")


def key(value):
    return value.replace(" ", "_").replace("-", "_")


def load_dgraph_users(client):
    txn = client.txn()
    try:
        users = []
        for row in read_csv("users.csv"):
            users.append({
                "uid": "_:user_" + row["user_id"],
                "dgraph.type": "User",
                "user_id": row["user_id"],
                "user_name": row["user_name"],
                "email": row["email"],
            })
        res = txn.mutate(set_obj=users)
        txn.commit()
        print("  Dgraph: usuarios cargados")
        return res.uids
    finally:
        txn.discard()


def load_dgraph_catalogs(client):
    txn = client.txn()
    try:
        data = []
        categories = set()
        regions = set()
        countries = set()
        for row in read_csv("destinations.csv"):
            if row["category"] not in categories:
                categories.add(row["category"])
                data.append({"uid": "_:category_" + key(row["category"]), "dgraph.type": "Category", "category_name": row["category"]})
            if row["region"] not in regions:
                regions.add(row["region"])
                data.append({"uid": "_:region_" + key(row["region"]), "dgraph.type": "Region", "name": row["region"]})
            if row["country"] not in countries:
                countries.add(row["country"])
                data.append({
                    "uid": "_:country_" + key(row["country"]),
                    "dgraph.type": "Country",
                    "name": row["country"],
                    "code": row["code"],
                    "region": {"uid": "_:region_" + key(row["region"])},
                })
            data.append({
                "uid": "_:destination_" + row["destination_id"],
                "dgraph.type": "Destination",
                "destination_id": row["destination_id"],
                "destination_name": row["destination_name"],
                "location": row["location"],
                "price": 0,
                "category": {"uid": "_:category_" + key(row["category"])},
                "pais": {"uid": "_:country_" + key(row["country"])},
            })
        res = txn.mutate(set_obj=data)
        txn.commit()
        print("  Dgraph: destinos y catalogos cargados")
        return res.uids
    finally:
        txn.discard()


def load_dgraph_hotels_activities(client, catalog_uids):
    txn = client.txn()
    try:
        data = []
        for row in read_csv("hotels.csv"):
            data.append({
                "uid": "_:hotel_" + row["hotel_id"],
                "dgraph.type": "Hotel",
                "hotel_id": row["hotel_id"],
                "hotel_name": row["hotel_name"],
                "stars": int(round(float(row["rating"]))),
                "price": float(row["price"]),
            })
            data.append({
                "uid": catalog_uids["destination_" + row["destination_id"]],
                "hospedaje": {"uid": "_:hotel_" + row["hotel_id"]},
            })
        for row in read_csv("activities.csv"):
            data.append({
                "uid": "_:activity_" + row["activity_id"],
                "dgraph.type": "Activity",
                "activity_id": row["activity_id"],
                "activity_name": row["activity_name"],
                "price": float(row["price"]),
            })
        for row in read_csv("hotel_activities.csv"):
            data.append({
                "uid": "_:hotel_" + row["hotel_id"],
                "tiene_actividad": {"uid": "_:activity_" + row["activity_id"]},
            })
        res = txn.mutate(set_obj=data)
        txn.commit()
        print("  Dgraph: hoteles y actividades cargados")
        return res.uids
    finally:
        txn.discard()


def load_dgraph_edges(client, user_uids, catalog_uids, object_uids):
    txn = client.txn()
    try:
        data = []
        for row in read_csv("friends.csv"):
            data.append({
                "uid": user_uids["user_" + row["user_id"]],
                "amigo": {"uid": user_uids["user_" + row["friend_id"]]},
            })
        for row in read_csv("reservations.csv"):
            if row["status"] == "confirmed":
                data.append({
                    "uid": user_uids["user_" + row["user_id"]],
                    "destino": {"uid": catalog_uids["destination_" + row["destination_id"]]},
                })
        for row in read_csv("user_activities.csv"):
            data.append({
                "uid": user_uids["user_" + row["user_id"]],
                "hizo_actividad": {"uid": object_uids["activity_" + row["activity_id"]]},
            })
        txn.mutate(set_obj=data)
        txn.commit()
        print("  Dgraph: relaciones cargadas")
    finally:
        txn.discard()


def load_dgraph(client):
    drop_dgraph(client)
    create_dgraph_schema(client)
    users = load_dgraph_users(client)
    catalogs = load_dgraph_catalogs(client)
    objects = load_dgraph_hotels_activities(client, catalogs)
    load_dgraph_edges(client, users, catalogs, objects)
    print("  Dgraph: datos cargados")


#Agreguen sus funciones de load de su base aqui!!!
def load_all(mongo_db, cassandra_session, dgraph_client):
    # Punto central para cargar todas las bases.
    load_mongo(mongo_db)
    load_cassandra(cassandra_session)
    load_dgraph(dgraph_client)
    print("  Carga completa")