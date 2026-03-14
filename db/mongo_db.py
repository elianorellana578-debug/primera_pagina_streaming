

from pymongo import MongoClient

# Conexión directa y forzada
db = MongoClient("mongodb+srv://test:contraelian@cluster0.xarfqvp.mongodb.net/?appName=Cluster0")

db_client = db.pelis

# El resto de tu código (create_user, etc.) se queda igual
