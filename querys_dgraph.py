import json

# ─── REQ 1 — Recomendación social de destinos ───────────────────────────────

def req1(client):
    username = input("Ingresa tu username: ").strip()

    query = """
    query rec_social($username: string)
    {
        rec_social(func: eq(user_name, $username)) {
            user_name
            amigo {
                user_name
                destino {
                    destination_name
                    price
                }
            }
        }
    }
    """
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 2 — Destinos populares por categoría ───────────────────────────────

def req2(client):
    category = input("Ingresa la categoría (playa, ciudad, montaña...): ").strip()

    query = """
    query destinos_populares($category: string)
    {
        destinos_populares(func: eq(category_name, $category)) {
            category_name
            ~category (orderdesc: count(~destino)) {
                destination_name
                location
                count(~destino)
            }
        }
    }
    """
    variables = {"$category": category}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 3 — Recomendación por región geográfica ────────────────────────────

def req3(client):
    region = input("Ingresa la región: ").strip()

    query = """
    query rec_region($region: string)
    {
        rec_region(func: eq(name, $region)) {
            name
            ~region {
                name
                code
                ~pais {
                    destination_name
                    location
                }
            }
        }
    }
    """
    variables = {"$region": region}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 4 — Actividades cercanas a un hotel ────────────────────────────────

def req4(client):
    hotel = input("Ingresa el nombre del hotel: ").strip()

    query = """
    query actividades_hotel($hotel: string)
    {
        actividades_hotel(func: eq(hotel_name, $hotel)) {
            hotel_name
            stars
            tieneActividad {
                activity_name
                price
            }
        }
    }
    """
    variables = {"$hotel": hotel}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 5 — Recomendación de actividades por amigos ────────────────────────

def req5(client):
    username = input("Ingresa tu username: ").strip()

    query = """
    query rec_actividades($username: string)
    {
        rec_actividades(func: eq(user_name, $username)) {
            user_name
            amigo {
                user_name
                hizoActividad {
                    activity_name
                    price
                }
            }
        }
    }
    """
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 6 — Destinos de la misma categoría ─────────────────────────────────

def req6(client):
    category = input("Ingresa la categoría (playa, ciudad, montaña...): ").strip()

    query = """
    query destinos_categoria($category: string)
    {
        destinos_categoria(func: eq(category_name, $category)) {
            category_name
            ~category {
                destination_name
                location
            }
        }
    }
    """
    variables = {"$category": category}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 7 — Destinos en el mismo país ──────────────────────────────────────

def req7(client):
    country = input("Ingresa el país: ").strip()

    query = """
    query destinos_pais($country: string)
    {
        destinos_pais(func: eq(name, $country)) {
            name
            code
            ~pais {
                destination_name
                location
                category {
                    category_name
                }
            }
        }
    }
    """
    variables = {"$country": country}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))


# ─── REQ 8 — Recomendación de amigos por gustos ─────────────────────────────

def req8(client):
    username = input("Ingresa tu username: ").strip()

    query = """
    query rec_amigos($username: string)
    {
        rec_amigos(func: eq(user_name, $username)) {
            user_name
            destino {
                category {
                    category_name
                    ~category {
                        ~destino {
                            user_name
                            email
                        }
                    }
                }
            }
        }
    }
    """
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    print(json.dumps(json.loads(res.json), indent=2))