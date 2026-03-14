
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas.schemes import Movie, UserCreate
from db.mongo_db import db_client
from crud.user_crud import create_user, user_str, get_movie_all, get_movie, verify_password
from model.models import user_model, user_model_all, usuario_model
from core.security import get_current_user, create_payoad

router = APIRouter()

@router.post("/sign_up")
async def sign_up(user: UserCreate):
    
    user_dict = user.model_dump()
    
    user = create_user(user_dict)
    
    return user

@router.post("/log_in")
async def log_in(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_client.user.find_one({"username": form_data.username})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro el usuario"
        )
    if not verify_password(plan_password=form_data.password, hashed_password=user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = create_payoad(data={"sub": form_data.username})
    return {"access_token": payload, "token_type": "bearer"}