from connect import connect_mongo, connect_cassandra, connect_dgraph


SECTIONS = [
    {
        "title": "Costos y Presupuesto",
        "queries": [
            ("Gasto promedio mensual del usuario", "Query 2", "MongoDB"),
            ("Ingresos totales por destino en el año", "Query 8", "MongoDB"),
            ("Tarifas de hotel por año", "Query 3", "Cassandra"),
            ("Ruta optima de viaje con escalas", "Query 2", "Dgraph"),
        ],
    },
    {
        "title": "Reservaciones",
        "queries": [
            ("Historial de reservaciones por ubicacion y periodo", "Query 1", "Cassandra"),
            ("Reservaciones recientes activas", "Query 2", "Cassandra"),
            ("Historial de cancelaciones", "Query 8", "Cassandra"),
            ("Itinerarios creados por un usuario", "Query 6", "MongoDB"),
        ],
    },
    {
        "title": "Destinos y Recomendaciones",
        "queries": [
            ("Recomendacion social de destinos", "Query 1", "Dgraph"),
            ("Recomendacion por region geografica", "Query 3", "Dgraph"),
            ("Destinos de la misma categoria", "Query 6", "Dgraph"),
            ("Destinos en el mismo pais", "Query 7", "Dgraph"),
            ("Paquetes turisticos por destino", "Query 1", "MongoDB"),
            ("Top 10 destinos mas vendidos", "Query 3", "MongoDB"),
        ],
    },
    {
        "title": "Actividades",
        "queries": [
            ("Actividades cercanas al hotel", "Query 4", "Dgraph"),
            ("Recomendacion de actividades por amigos", "Query 5", "Dgraph"),
            ("Catalogo de actividades por destino", "Query 5", "Cassandra"),
            ("Actividades realizadas por reserva", "Query 7", "Cassandra"),
        ],
    },
    {
        "title": "Hoteles y Hospedaje",
        "queries": [
            ("Top 10 hoteles mejor ranqueados por presupuesto", "Query 5", "MongoDB"),
            ("Disponibilidad inmediata para destino", "Query 6", "Cassandra"),
        ],
    },
    {
        "title": "Vuelos y Aerolineas",
        "queries": [
            ("Vuelos por rango de precio", "Query 7", "MongoDB"),
            ("Ciudades por aerolinea", "Query 8", "Dgraph"),
        ],
    },
    {
        "title": "Usuarios y Viajeros",
        "queries": [
            ("Ranking de viajeros frecuentes", "Query 4", "MongoDB"),
            ("Busquedas de usuario por rango de fechas", "Query 4", "Cassandra"),
        ],
    },
]



#  Carga y borrado de datos una sola accion para las 3 bases


def cargar_datos(mongo_db, cassandra_session, dgraph_client):
    print("\n  Esto cargara la informacion a la base de datos")
    confirm = input("  Deseas continuar? (s/n): ")
    if confirm.lower() != "s":
        return

    print("  Cargando datos...")

    print("  Datos cargados exitosamente.")


def borrar_datos(mongo_db, cassandra_session, dgraph_client):
    print("\n  Atencion: Esto eliminara TODOS los datos de la base.")
    confirm = input("  Estas seguro? (s/n): ")
    if confirm.lower() != "s":
        return

    print("  Borrando datos...")
    # TODO: drop_mongo(mongo_db)
    # TODO: drop_cassandra(cassandra_session)
    # TODO: drop_dgraph(dgraph_client)
    print("  Datos eliminados exitosamente.")


def run_query(name, qid, db, mongo_db, cassandra_session, dgraph_client):
    print(f"\n>>> {name}")
    print("-" * 40)

    # MongoDB
    if db == "MongoDB" and qid == "Query 1":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 2":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 3":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 4":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 5":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 6":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 7":
        print("Pendiente de implementar")
    elif db == "MongoDB" and qid == "Query 8":
        print("Pendiente de implementar")

    # Cassandra
    elif db == "Cassandra" and qid == "Query 1":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 2":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 3":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 4":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 5":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 6":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 7":
        print("Pendiente de implementar")
    elif db == "Cassandra" and qid == "Query 8":
        print("Pendiente de implementar")

    # Dgraph
    elif db == "Dgraph" and qid == "Query 1":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 2":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 3":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 4":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 5":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 6":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 7":
        print("Pendiente de implementar")
    elif db == "Dgraph" and qid == "Query 8":
        print("Pendiente de implementar")


def main():
    mongo_db = connect_mongo()
    cassandra_session = connect_cassandra()
    dgraph_client, dgraph_stub = connect_dgraph()

    total_sections = len(SECTIONS)

    while True:
        print("\n=== Travel Reservations Platform ===")
        for i, section in enumerate(SECTIONS, 1):
            print(f"{i}. {section['title']}")
        print(f"{total_sections + 1}. Cargar datos")
        print(f"{total_sections + 2}. Borrar datos")
        print(f"{total_sections + 3}. Salir")

        option = input("\nSelecciona una opcion: ")

        if option == str(total_sections + 3):
            dgraph_stub.close()
            print("Saliendo...")
            break

        if option == str(total_sections + 1):
            cargar_datos(mongo_db, cassandra_session, dgraph_client)
            continue

        if option == str(total_sections + 2):
            borrar_datos(mongo_db, cassandra_session, dgraph_client)
            continue

        if not option.isdigit() or int(option) < 1 or int(option) > total_sections:
            print("Opcion invalida.")
            continue

        section = SECTIONS[int(option) - 1]

        while True:
            print(f"\n--- {section['title']} ---")
            for i, (name, qid, db) in enumerate(section["queries"], 1):
                print(f"{i}. {name}")
            print(f"{len(section['queries']) + 1}. Regresar")

            sub = input("\nSelecciona una consulta: ")

            if sub == str(len(section["queries"]) + 1):
                break

            if not sub.isdigit() or int(sub) < 1 or int(sub) > len(section["queries"]):
                print("Opcion invalida.")
                continue

            name, qid, db = section["queries"][int(sub) - 1]
            run_query(name, qid, db, mongo_db, cassandra_session, dgraph_client)


if __name__ == "__main__":
    main()