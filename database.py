from pymongo import MongoClient
import certifi

MONGO_URI = 'mongodb+srv://team_python:BZKWmgypKZETgBx1@cluster0.i6t3kmq.mongodb.net/?retryWrites=true&w=majority'

ca = certifi.where()
def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client.hotel_python  # Acceder a la base de datos como un atributo del cliente
    except ConnectionError:
        print("Error de conexión con la base de datos")
    return db
