
from fastapi import HTTPException, status
from db.mongo_db import db_client
from model.models import user_model
from model.models import user_model, user_model_all, usuario_model, usuario_model_all
from schemas.schemes import UserOut
import bcrypt

def create_movie(movie):
    db = db_client.movie.insert_one(movie)
    return db.inserted_id

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt)

def verify_password(plan_password, hashed_password):
    return bcrypt.checkpw(plan_password.encode("utf-8"), hashed_password)

def create_user(user):
    # Verificamos si el email O el username ya existen
    if db_client.user.find_one({"email": user.get("email")}):
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    if db_client.user.find_one({"username": user.get("username")}):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    user_copy = user.copy()
    user_copy["password"] = hash_password(user["password"])
    
    result = db_client.user.insert_one(user_copy)
    usuario = db_client.user.find_one({"_id": result.inserted_id})
    
    # Retornamos sin campos sensibles
    return usuario_model(usuario)

def user_str(id):
    user = db_client.movie.find_one({"_id": id})
    return user_model(user)

def get_movie_all():
    movies = db_client.movie.find({})
    return user_model_all(movies)

def get_users_all():
    users = db_client.user.find({})
    return usuario_model_all(users)

def get_movie(title):
    try:
        movie = db_client.movie.find_one({"title": title})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error con la base de datos"
        )
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La pelicula {title} no se encontro"
        )
    return user_model(movie)

