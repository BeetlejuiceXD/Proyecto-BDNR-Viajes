# **Proyecto-BDNR-Viajes**

Heriberto Vlaminck Salinas 753987
Jair Ernesto Aguilar Limon 746023


---

# **Instrucciones**


---

## Levantar bases de datos con Docker

Asegúrate de tener Docker instalado y corriendo.

### MongoDB
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

### Cassandra
```bash
docker run -d -p 9042:9042 --name cassandra cassandra
```

### Dgraph , solo instalar el primero si ya tienes ratel
```bash
docker run -d -p 8080:8080 -p 9080:9080 --name dgraph dgraph/standalone

docker run --name ratel -d -p 8000:8000 dgraph/ratel:latest
```

---

### 1. Crear el entorno virtual

```bash
python3 -m venv PBNR-Viajes
```

### 2. Activar el entorno virtual

#### En macOS / Linux:
```bash
source PBNR-Viajes/bin/activate
```

#### En Windows:
```bash
PBNR-Viajes\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---



## ▶️ Ejecutar el proyecto

### Correr bases de datos
```bash
docker start "nombre de tu contenedor"
```

```bash
python3 main.py
```

## **Descripcion del proyecto**




