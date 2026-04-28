# **Proyecto-BDNR-Viajes**

Heriberto Vlaminck Salinas 753987
Jair Ernesto Aguilar Limon 746023
Josue Godoy Orozco 752666


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

La aplicación funciona como un sistema que centraliza 3 diferentes bases de datos no relaciones, siendo cassandra, mongodb y Dgraph, donde la vista a el usuario pueda buscar destinos, consultar opciones de actividades y hoteles e informacion relevantes de viajes realizados, o que se desean realizar. Además, se incluyen funcionalidades de recomendación basadas en relaciones entre destinos y preferencias del usuario, así como el registro del historial de búsquedas y reservaciones de manera historica. 




