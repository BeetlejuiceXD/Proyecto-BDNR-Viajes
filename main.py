from connect import connect_mongo, connect_cassandra, connect_dgraph
from populate import load_all, drop_mongo, drop_cassandra, drop_dgraph
from Mongodb import querys_mongodb
from Dgraph import querys_dgraph


def cargar_datos(mongo_db, cassandra_session, dgraph_client):
    # Preguntamos antes de cargar datos en las tres bases.
    print("\nEsto cargara los datos en MongoDB, Cassandra y Dgraph")
    confirm = input("Deseas continuar? (s/n): ")
    if confirm.lower() == "s":
        load_all(mongo_db, cassandra_session, dgraph_client)
        print("Datos cargados")
    else:
        print("Carga cancelada")


def borrar_datos(mongo_db, cassandra_session, dgraph_client):
    # Preguntamos antes de borrar datos de las tres bases.
    print("\nEsto borrara los datos de MongoDB, Cassandra y Dgraph")
    confirm = input("Estas seguro? (s/n): ")
    if confirm.lower() == "s":
        drop_mongo(mongo_db)
        drop_cassandra(cassandra_session)
        drop_dgraph(dgraph_client)
        print("Datos borrados")
    else:
        print("Borrado cancelado")


def main():
    # Abrimos conexiones al iniciar el programa.
    mongo_db = connect_mongo()
    cassandra_session = connect_cassandra()
    dgraph_client, dgraph_stub = connect_dgraph()

    while True:
        # Menu principal.
        print("\nTravel Reservations")
        print("1. Cargar datos (todas las bases)")
        print("2. Secciones (queries)")
        print("3. Borrar datos (todas las bases)")
        print("4. Salir")

        option = input("\nSelecciona una opcion: ")

        if option == "1":
            cargar_datos(mongo_db, cassandra_session, dgraph_client)

        elif option == "2":
            # Este bloque muestra las secciones de consultas.
            while True:
                print("\n--- SECCIONES ---")
                print("1. Costos y Presupuesto")
                print("2. Reservaciones")
                print("3. Destinos y Recomendaciones")
                print("4. Actividades")
                print("5. Hoteles y Hospedaje")
                print("6. Vuelos y Aerolineas")
                print("7. Usuarios y Viajeros")
                print("8. Regresar")

                section_option = input("\nSelecciona una seccion: ")

                if section_option == "1":
                    # Consultas de costos y presupuesto.
                    while True:
                        print("\n--- Costos y Presupuesto ---")
                        print("1. Gasto promedio mensual del usuario Query 2 MongoDB")
                        print("2. Ingresos totales por destino en el ano Query 8 MongoDB")
                        print("3. Tarifas de hotel por ano Query 3 Cassandra")
                        print("4. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Gasto promedio mensual del usuario Query 2 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_gasto_promedio(mongo_db)
                        elif query_option == "2":
                            print("\n>>> Ingresos totales por destino en el ano Query 8 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_ingresos_destino(mongo_db)
                        elif query_option == "3":
                            print("\n>>> Tarifas de hotel por ano Query 3 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_tarifas_hotel(cassandra_session)
                        elif query_option == "4":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "2":
                    # Consultas de reservaciones.
                    while True:
                        print("\n--- Reservaciones ---")
                        print("1. Historial de reservaciones por ubicacion y periodo Query 1 Cassandra")
                        print("2. Reservaciones recientes activas Query 2 Cassandra")
                        print("3. Itinerarios creados por un usuario Query 6 MongoDB")
                        print("4. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Historial de reservaciones por ubicacion y periodo Query 1 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_reservaciones_ubicacion(cassandra_session)
                        elif query_option == "2":
                            print("\n>>> Reservaciones recientes activas Query 2 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_reservaciones_activas(cassandra_session)
                        elif query_option == "3":
                            print("\n>>> Itinerarios creados por un usuario Query 6 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_itinerarios_usuario(mongo_db)
                        elif query_option == "4":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "3":
                    # Consultas de destinos y recomendaciones.
                    while True:
                        print("\n--- Destinos y Recomendaciones ---")
                        print("1. Recomendacion social de destinos Query 1 Dgraph")
                        print("2. Destinos populares por categoria Query 2 Dgraph")
                        print("3. Recomendacion por region geografica Query 3 Dgraph")
                        print("4. Destinos de la misma categoria Query 6 Dgraph")
                        print("5. Destinos en el mismo pais Query 7 Dgraph")
                        print("6. Paquetes turisticos por destino Query 1 MongoDB")
                        print("7. Top 10 destinos mas vendidos Query 3 MongoDB")
                        print("8. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Recomendacion social de destinos Query 1 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req1(dgraph_client)
                        elif query_option == "2":
                            print("\n>>> Destinos populares por categoria Query 2 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req2(dgraph_client)
                        elif query_option == "3":
                            print("\n>>> Recomendacion por region geografica Query 3 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req3(dgraph_client)
                        elif query_option == "4":
                            print("\n>>> Destinos de la misma categoria Query 6 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req6(dgraph_client)
                        elif query_option == "5":
                            print("\n>>> Destinos en el mismo pais Query 7 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req7(dgraph_client)
                        elif query_option == "6":
                            print("\n>>> Paquetes turisticos por destino Query 1 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_paquetes_por_destino(mongo_db)
                        elif query_option == "7":
                            print("\n>>> Top 10 destinos mas vendidos Query 3 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_top_destinos(mongo_db)
                        elif query_option == "8":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "4":
                    # Consultas de actividades.
                    while True:
                        print("\n--- Actividades ---")
                        print("1. Actividades cercanas al hotel Query 4 Dgraph")
                        print("2. Recomendacion de actividades por amigos Query 5 Dgraph")
                        print("3. Catalogo de actividades por destino Query 5 Cassandra")
                        print("4. Actividades realizadas por reserva Query 7 Cassandra")
                        print("5. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Actividades cercanas al hotel Query 4 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req4(dgraph_client)
                        elif query_option == "2":
                            print("\n>>> Recomendacion de actividades por amigos Query 5 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req5(dgraph_client)
                        elif query_option == "3":
                            print("\n>>> Catalogo de actividades por destino Query 5 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_actividades_destino(cassandra_session)
                        elif query_option == "4":
                            print("\n>>> Actividades realizadas por reserva Query 7 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_actividades_reserva(cassandra_session)
                        elif query_option == "5":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "5":
                    # Consultas de hoteles y hospedaje.
                    while True:
                        print("\n--- Hoteles y Hospedaje ---")
                        print("1. Top 10 hoteles mejor ranqueados por presupuesto Query 5 MongoDB")
                        print("2. Disponibilidad inmediata para destino Query 6 Cassandra")
                        print("3. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Top 10 hoteles mejor ranqueados por presupuesto Query 5 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_top_hoteles(mongo_db)
                        elif query_option == "2":
                            print("\n>>> Disponibilidad inmediata para destino Query 6 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_disponibilidad_destino(cassandra_session)
                        elif query_option == "3":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "6":
                    # Consultas de vuelos y aerolineas.
                    while True:
                        print("\n--- Vuelos y Aerolineas ---")
                        print("1. Vuelos por rango de precio Query 7 MongoDB")
                        print("2. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Vuelos por rango de precio Query 7 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_vuelos_rango(mongo_db)
                        elif query_option == "2":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "7":
                    # Consultas de usuarios y viajeros.
                    while True:
                        print("\n--- Usuarios y Viajeros ---")
                        print("1. Ranking de viajeros frecuentes Query 4 MongoDB")
                        print("2. Busquedas de usuario por rango de fechas Query 4 Cassandra")
                        print("3. Recomendacion de amigos por gustos Query 8 Dgraph")
                        print("4. Regresar")

                        query_option = input("\nSelecciona una consulta: ")

                        if query_option == "1":
                            print("\n>>> Ranking de viajeros frecuentes Query 4 MongoDB")
                            print("-" * 40)
                            querys_mongodb.query_ranking_viajeros(mongo_db)
                        elif query_option == "2":
                            print("\n>>> Busquedas de usuario por rango de fechas Query 4 Cassandra")
                            print("-" * 40)
                            querys_cassandra.query_busquedas_usuario(cassandra_session)
                        elif query_option == "3":
                            print("\n>>> Recomendacion de amigos por gustos Query 8 Dgraph")
                            print("-" * 40)
                            querys_dgraph.req8(dgraph_client)
                        elif query_option == "4":
                            break
                        else:
                            print("Opcion invalida")

                elif section_option == "8":
                    break
                else:
                    print("Opcion invalida")

        elif option == "3":
            borrar_datos(mongo_db, cassandra_session, dgraph_client)

        elif option == "4":
            # Cerramos Dgraph antes de salir.
            dgraph_stub.close()
            print("Saliendo...")
            break

        else:
            print("Opcion invalida")


if __name__ == "__main__":
    main()
