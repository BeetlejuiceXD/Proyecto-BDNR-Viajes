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


# =====================================================
#                    DGRAPH
# =====================================================
def drop_dgraph(client):
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)
    print("  Dgraph: todo borrado")
def create_dgraph_schema(client):
    schema = """
    # User 
    user_name:        string  @index(hash) .
    email:            string  @index(hash) .

    # Destination 
    destination_name: string  @index(hash) .
    price:            float                .
    location:         string  @index(hash) .

    # Activity 
    activity_name:    string  @index(hash) .

    # Hotel 
    hotel_name:       string  @index(hash) .
    stars:            int                  .

    # Category 
    category_name:    string  @index(hash) .

    # Country 
    name:             string  @index(hash) .
    code:             string               .

    # Relaciones 
    amigo:            [uid]                              .
    destino:          [uid]  @reverse @count             .
    hizo_actividad:   [uid]                              .
    category:         uid    @reverse                    .
    pais:             uid    @reverse                    .
    hospedaje:        [uid]                              .
    tiene_actividad:  [uid]                              .
    region:           uid    @reverse                    .

    #Tipos 
    type User {
        user_name
        email
        amigo
        destino
        hizo_actividad
    }

    type Destination {
        destination_name
        price
        location
        category
        pais
        hospedaje
    }

    type Activity {
        activity_name
        price
    }

    type Hotel {
        hotel_name
        stars
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


#Agreguen sus funciones de load de su base aqui!!!
def load_all(mongo_db, cassandra_session, dgraph_client):
    # Punto central para cargar todas las bases.
    load_mongo(mongo_db)
    print("  Carga completa")