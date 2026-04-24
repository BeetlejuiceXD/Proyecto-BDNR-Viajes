from pymongo import MongoClient
from cassandra.cluster import Cluster
import pydgraph


def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["travel_reservations"]
    return db


def connect_cassandra():
    cluster = Cluster(["127.0.0.1"])
    session = cluster.connect()

    session.execute("""
        CREATE KEYSPACE IF NOT EXISTS travel_reservations
        WITH replication = {
            'class': 'SimpleStrategy',
            'replication_factor': 1
        }
    """)

    session.set_keyspace("travel_reservations")
    return session


def connect_dgraph():
    client_stub = pydgraph.DgraphClientStub("localhost:9080")
    client = pydgraph.DgraphClient(client_stub)
    return client, client_stub

