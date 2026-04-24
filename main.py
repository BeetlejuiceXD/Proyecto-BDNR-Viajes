from connect import connect_mongo, connect_cassandra, connect_dgraph

def main():

    mongo_db = connect_mongo()

    cassandra_session = connect_cassandra()

    dgraph_client, dgraph_stub = connect_dgraph()

    while True:

        print("\n=== Travel Reservations Platform ===")

        print("1. Cassandra")

        print("2. MongoDB")

        print("3. Dgraph")

        print("4. Salir")

        option = input("Selecciona una opción: ")

        if option == "1":

            print("Menú de Cassandra pendiente.")

        elif option == "2":

            print("Menú de MongoDB pendiente.")

        elif option == "3":

            print("Menú de Dgraph pendiente.")

        elif option == "4":

            dgraph_stub.close()

            print("Saliendo...")

            break

        else:

            print("Opción inválida.")

if __name__ == "__main__":

    main()