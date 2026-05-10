import csv
import json
import pydgraph
from datetime import datetime

def drop_dgraph(client):
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)
    print("  Dgraph: todo borrado")