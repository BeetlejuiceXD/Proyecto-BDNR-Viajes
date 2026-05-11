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

