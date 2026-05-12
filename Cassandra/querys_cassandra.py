import logging
from datetime import datetime

# Set logger
log = logging.getLogger()


def get_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def show_date(value):
    try:
        return value.date().strftime("%Y-%m-%d")
    except AttributeError:
        return str(value)


# Req 1 - Historial de reservaciones por usuario, destino y periodo
SELECT_RESERVACIONES_LUGAR = """
    SELECT user_id, destination_name, date, reservation_id, cost
    FROM reservaciones_lugar
    WHERE user_id = ? AND destination_name = ? AND date >= ? AND date <= ?
"""

# Req 2 - Reservaciones por estado
SELECT_RESERVACIONES_POR_ESTADO = """
    SELECT user_id, status, reservation_time, reservation_id, destination_name, hotel_name, id_flight
    FROM reservaciones_por_estado
    WHERE user_id = ? AND status = ?
"""

# Req 3 - Tarifas de hotel
SELECT_TARIFAS_HOTEL = """
    SELECT hotel_name, date, room_type, price
    FROM tarifas_hotel
    WHERE hotel_name = ?
"""

# Req 4 - Busquedas de usuario por rango de fechas
SELECT_BUSQUEDAS_USUARIO = """
    SELECT user_id, search_time, destination_name, departure_city, travelers_count
    FROM busquedas_usuario
    WHERE user_id = ? AND search_time >= ? AND search_time <= ?
"""

# Req 5 - Catalogo de actividades por destino
SELECT_CATALOGO_ACTIVIDADES = """
    SELECT destination_id, category, activity_name, price
    FROM catalogo_actividades
    WHERE destination_id = ?
"""
# Req 6 - Disponibilidad de hoteles por destino
SELECT_DISPONIBILIDAD_HOTELES = """
    SELECT hotel_id, hotel_name, available_rooms, start_date, end_date
    FROM disponibilidad_hoteles
    WHERE destination_id = ?
"""

# Req 7 - Actividades realizadas por reserva
SELECT_ACTIVIDADES_RESERVA = """
    SELECT reservation_id, activity_name, category
    FROM actividades_reserva
    WHERE reservation_id = ?
"""
# Req 8 - Historial de cancelaciones por usuario
SELECT_HISTORIAL_CANCELACIONES = """
    SELECT user_id, status, reservation_time, reservation_id, destination_name, hotel_name, id_flight
    FROM reservaciones_por_estado
    WHERE user_id = ? AND status = 'cancelled'
"""


# Req 1
def query_reservaciones_ubicacion(session):
    user_id = input("ID del usuario (ej: U001): ")
    destination_name = input("Destino: ")
    f1 = input("Fecha inicio (AAAA-MM-DD): ")
    f2 = input("Fecha fin (AAAA-MM-DD): ")

    log.info(f"Buscando reservaciones de {user_id} en {destination_name}")
    stmt = session.prepare(SELECT_RESERVACIONES_LUGAR)
    rows = session.execute(stmt, [user_id, destination_name, get_date(f1), get_date(f2)])
    for r in rows:
        print(f"user_id={r.user_id}, destination_name={r.destination_name}, date={show_date(r.date)}, reservation_id={r.reservation_id}, cost={r.cost}")


# Req 2
def query_reservaciones_activas(session):
    user_id = input("ID del usuario (ej: U001): ")
    status = input("Estado (confirmed/active/cancelled): ")

    log.info(f"Buscando reservaciones de {user_id} con estado {status}")
    stmt = session.prepare(SELECT_RESERVACIONES_POR_ESTADO)
    rows = session.execute(stmt, [user_id, status])
    for r in rows:
        print(f"user_id={r.user_id}, status={r.status}, reservation_time={show_date(r.reservation_time)}, reservation_id={r.reservation_id}, destination_name={r.destination_name}, hotel_name={r.hotel_name}, id_flight={r.id_flight}")


# Req 3
def query_tarifas_hotel(session):
    hotel_name = input("Nombre del hotel: ")

    log.info(f"Consultando tarifas de {hotel_name}")
    stmt = session.prepare(SELECT_TARIFAS_HOTEL)
    rows = session.execute(stmt, [hotel_name])
    for r in rows:
        print(f"hotel_name={r.hotel_name}, date={show_date(r.date)}, room_type={r.room_type}, price={r.price}")


# Req 4
def query_busquedas_usuario(session):
    user_id = input("ID del usuario (ej: U001): ")
    f1 = input("Fecha inicio (AAAA-MM-DD): ")
    f2 = input("Fecha fin (AAAA-MM-DD): ")

    log.info(f"Consultando busquedas de {user_id}")
    stmt = session.prepare(SELECT_BUSQUEDAS_USUARIO)
    rows = session.execute(stmt, [user_id, get_date(f1), get_date(f2)])
    for r in rows:
        print(f"user_id={r.user_id}, search_time={show_date(r.search_time)}, destination_name={r.destination_name}, departure_city={r.departure_city}, travelers_count={r.travelers_count}")


# Req 5
def query_actividades_destino(session):
    destination_id = input("ID del destino (ej: D001): ")

    log.info(f"Consultando catalogo de {destination_id}")
    stmt = session.prepare(SELECT_CATALOGO_ACTIVIDADES)
    rows = session.execute(stmt, [destination_id])
    for r in rows:
        print(f"destination_id={r.destination_id}, category={r.category}, activity_name={r.activity_name}, price={r.price}")
# Req 6
def query_disponibilidad_destino(session):
    destination_id = input("ID del destino (ej: D001): ")

    log.info(f"Consultando disponibilidad en {destination_id}")
    stmt = session.prepare(SELECT_DISPONIBILIDAD_HOTELES)
    rows = session.execute(stmt, [destination_id])
    for r in rows:
        print(f"hotel_id={r.hotel_id}, hotel_name={r.hotel_name}, available_rooms={r.available_rooms}, start_date={show_date(r.start_date)}, end_date={show_date(r.end_date)}")


# Req 7
def query_actividades_reserva(session):
    reservation_id = input("ID de reservacion (ej: R001): ")

    log.info(f"Listando actividades de reserva {reservation_id}")
    stmt = session.prepare(SELECT_ACTIVIDADES_RESERVA)
    rows = session.execute(stmt, [reservation_id])
    for r in rows:
        print(f"reservation_id={r.reservation_id}, activity_name={r.activity_name}, category={r.category}")


# Req 8
def query_historial_cancelaciones(session):
    user_id = input("ID del usuario (ej: U001): ")

    log.info(f"Consultando cancelaciones de {user_id}")
    stmt = session.prepare(SELECT_HISTORIAL_CANCELACIONES)
    rows = session.execute(stmt, [user_id])
    for r in rows:
        print(f"reservation_id={r.reservation_id}, reservation_time={show_date(r.reservation_time)}, status={r.status}")