
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import StreamingResponse
from schemas.schemes import Movie, UserCreate, UserOut
from db.mongo_db import db_client
from crud.user_crud import create_movie, create_user, user_str, get_movie_all, get_movie, get_users_all
from model.models import user_model, user_model_all
from core.security import get_current_user
import os
from bson import ObjectId
from datetime import datetime, timezone, timedelta

router = APIRouter()

@router.get("/movies")
async def movies():
    return get_movie_all()

@router.get("/movies/privado")
async def movies(token: UserOut = Depends(get_current_user)):
    return token

@router.get("/movies/{name_movie}")
async def movies(name_movie: str):
    movie = name_movie.capitalize()
    return get_movie(title=movie)

@router.get("/movies/search/{title}")
async def search(title: str):
    movie = db_client.movie.find_one({"title": title.capitalize()})
    del movie["_id"] 
    return movie

@router.get("/users")
async def users():
    return get_users_all()





VIDEO_PATH = "videos/"

# @router.get("/video/{video_name}")
# async def stream_video(video_name: str):
#     file_path = os.path.join(VIDEO_PATH, f"{video_name}.mp4")
    
#     if not os.path.exists(file_path):
#         raise HTTPException(status_code=404, detail="Video no encontrado")

#     # Función generadora que lee el archivo en bloques (ej. 1MB por vez)
#     def iterfile():
#         with open(file_path, mode="rb") as file_like:
#             yield from file_like

#     # Enviamos el video con el tipo de contenido correcto
#     return StreamingResponse(iterfile(), media_type="video/mp4")


# ... (tus otros imports se mantienen igual)

# Optimización del streaming para carga rápida
@router.get("/video/{video_name}")
async def stream_video(video_name: str):
    file_path = os.path.join(VIDEO_PATH, f"{video_name}.mp4")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video no encontrado")

    def iterfile():
        # 1MB es ideal para que el reproductor empiece rápido
        TAMANO_BLOQUE = 1024 * 1024 
        with open(file_path, mode="rb") as file_like:
            while True:
                chunk = file_like.read(TAMANO_BLOQUE)
                if not chunk:
                    break
                yield chunk

    return StreamingResponse(iterfile(), media_type="video/mp4")

# Búsqueda por ID con manejo de errores de formato
@router.get("/movies/id/{movie_id}")
async def detalle_por_id(movie_id: str):
    clean_id = movie_id.strip() 
    try:
        movie = db_client.movie.find_one({"_id": ObjectId(clean_id)})
    except:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
        
    if not movie:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    return user_model(movie)

# Historial con corrección de inserción asíncrona (si no usas motor)
@router.post("/history/{movie_id}")
async def add_to_history(movie_id: str, current_user: UserOut = Depends(get_current_user)):
    try:
        movie = db_client.movie.find_one({"_id": ObjectId(movie_id)})
    except:
        raise HTTPException(status_code=400, detail="ID de película inválido")

    if not movie:
        raise HTTPException(status_code=404, detail="Película no encontrada")

    history_entry = {
        "username": current_user.username,
        "movie_id": movie_id,
        "movie_title": movie["title"],
        "watched_at": datetime.now(timezone.utc)
    }
    
    db_client.history.insert_one(history_entry)
    return {"message": "Historial actualizado"}



@router.delete("/delete/{title}")
async def delete(title: str):
    movie_delete = db_client.movie.find_one_and_delete({"title": title.capitalize()})
    if movie_delete:
        return {"msg": "La pelicual ha sido eliminada"}
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="No se encontro la pelicula"
    )

