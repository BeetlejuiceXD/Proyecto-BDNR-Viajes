import csv
import json
import pydgraph
from datetime import datetime



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