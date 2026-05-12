# Req 1 - Paquetes turisticos por destino
def query_paquetes_por_destino(db):
    # Buscamos paquetes que coinciden con el destino escrito.
    destino = input("Nombre del destino: ")
    resultados = db.packages.find(
        {"destination_name": destino},
        {"_id": 0, "package_id": 1, "destination_name": 1, "hotel_name": 1,
         "location": 1, "airline_name": 1, "final_price": 1}
    )
    count = 0
    for r in resultados:
        print(r)
        count += 1
    if count == 0:
        print("No se encontraron paquetes para ese destino")


# Req 2 - Gasto promedio anual del usuario
def query_gasto_promedio(db):
    # Pedimos usuario y año para calcular su gasto mensual promedio.
    user_id = input("ID del usuario (ej: U001): ")
    year = int(input("Año (ej: 2026): "))

    # El pipeline filtra reservaciones y agrupa por año
    pipeline = [
    {"$match": {"user_id": user_id, "year": year, "status": "confirmed"}},
    {"$group": {
        "_id": "$user_id",
        "yearly_average": {"$avg": "$price"},
        "total_spent": {"$sum": "$price"},
        "reservation_count": {"$sum": 1}
    }},
    {"$project": {
        "_id": 0,
        "user_id": "$_id",
        "year": year,
        "yearly_average": 1,
        "total_spent": 1,
        "reservation_count": 1
    }}
    ]

    resultados = list(db.reservations.aggregate(pipeline))
    if resultados:
        for r in resultados:
            print(r)
    else:
        print("No se encontraron reservaciones para ese usuario y año")


# Req 3 - Top 10 destinos mas vendidos por temporada
def query_top_destinos(db):
    # Filtramos por temporada y contamos ventas confirmadas.
    season = input("Temporada (spring/summer/fall/winter): ")

    pipeline = [
        {"$match": {"season": season, "status": "confirmed"}},
        {"$group": {
            "_id": {"destination_name": "$destination_name", "season": "$season"},
            "sales": {"$sum": 1},
            "price": {"$avg": "$price"}
        }},
        {"$sort": {"sales": -1, "price": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "destination_name": "$_id.destination_name",
            "price": 1,
            "sales": 1,
            "season": "$_id.season"
        }}
    ]
    resultados = list(db.reservations.aggregate(pipeline))
    for r in resultados:
        print(r)
    if not resultados:
        print("No se encontraron resultados")


# Req 4 - Ranking de viajeros frecuentes y su mayor gasto
def query_ranking_viajeros(db):
    # Agrupamos reservas confirmadas para encontrar viajeros frecuentes.
    pipeline = [
        {"$match": {"status": "confirmed"}},
        {"$sort": {"user_id": 1, "price": -1}},
        {"$group": {
            "_id": {"user_id": "$user_id", "user_name": "$user_name"},
            "trip_count": {"$sum": 1},
            "destination_name": {"$first": "$destination_name"},
            "price": {"$first": "$price"}
        }},
        {"$sort": {"trip_count": -1, "price": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "user_name": "$_id.user_name",
            "trip_count": 1,
            "destination_name": 1,
            "price": 1
        }}
    ]
    resultados = list(db.reservations.aggregate(pipeline))
    for r in resultados:
        print(r)


# Req 5 - Top 10 hoteles mejor ranqueados por presupuesto
def query_top_hoteles(db):
    # Filtramos hoteles por rango y ordenamos por rating.
    rango = input("Rango de precio (low/medium/high/luxury): ")

    pipeline = [
        {"$match": {"price_range": rango}},
        {"$sort": {"rating": -1}},
        {"$limit": 10},
        {"$project": {"_id": 0, "hotel_name": 1, "rating": 1, "price_range": 1}}
    ]
    resultados = list(db.hotels.aggregate(pipeline))
    for r in resultados:
        print(r)
    if not resultados:
        print("No se encontraron hoteles en ese rango")


# Req 6 - Itinerarios creados por un usuario
def query_itinerarios_usuario(db):
    # Mostramos itinerarios guardados para un usuario.
    user_id = input("ID del usuario (ej: U001): ")
    resultados = db.itineraries.find(
        {"user_id": user_id},
        {"_id": 0,"destination_id":0},
        
    )
    count = 0
    for r in resultados:
        print(r)
        count += 1
    if count == 0:
        print("No se encontraron itinerarios para ese usuario")


# Req 7 - Vuelos por rango de precio
def query_vuelos_rango(db):
    # Buscamos vuelos dentro de un rango de precio.
    min_p = float(input("Precio minimo: "))
    max_p = float(input("Precio maximo: "))
    resultados = db.flights.find(
        {"price": {"$gte": min_p, "$lte": max_p}},
        {"_id": 0, "id_flight": 1, "airline": 1, "origin": 1,
         "destination_name": 1, "departure_date": 1, "price": 1, "available_seats": 1}
    ).sort("price", 1)
    count = 0
    for r in resultados:
        if "departure_date" in r:
            r["departure_date"] = str(r["departure_date"])
        print(r)
        count += 1
    if count == 0:
        print("No se encontraron vuelos en ese rango")


# Req 8 - Ingresos totales por destino en el ano
def query_ingresos_destino(db):
    # Sumamos ingresos por destino en el ano indicado.
    year = int(input("Año (ej: 2026): "))

    pipeline = [
        {"$match": {"year": year, "status": "confirmed"}},
        {"$group": {
            "_id": {"destination_name": "$destination_name", "year": "$year"},
            "total_revenue": {"$sum": "$price"},
            "total_reservations": {"$sum": 1}
        }},
        {"$sort": {"total_revenue": -1}},
        {"$project": {
            "_id": 0,
            "destination_name": "$_id.destination_name",
            "total_revenue": 1,
            "year": "$_id.year",
            "total_reservations": 1
        }}
    ]
    resultados = list(db.reservations.aggregate(pipeline))
    for r in resultados:
        print(r)
    if not resultados:
        print("No se encontraron resultados")
