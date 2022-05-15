# Proiectus
Proyecto final para la clase de Diseño y Arquitectura de Software TC3049, en el Tec de Monterrey.


# Requisitos

Agregar un archivo .env con los valores solicitados en el .env.sample (por ahora solo se necesita la connection string para mongo).

# Ejecución local

1. Instalar dependencias

```
cd src
pip install requirements.txt
```

2. Ejecutar el servidor (desde la carpeta src)

```
uvicorn main:app --reload
```

La aplicación comenzará a correr en `http://127.0.0.1:8000/`


# Ejecución con Docker

```
docker-compose up -d
```