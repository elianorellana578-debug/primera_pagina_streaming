
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from db.mongo_db import db_client
from schemas.schemes import UserOut

KEY_SECRET = "fjdklfjlkf"
ALGORITH = "HS256"
DURATION = 30 # Minutos

oauth2 = OAuth2PasswordBearer(tokenUrl="/log_in")

def create_payoad(data: dict):
    try:
        data_copy = data.copy()
        # Usamos siempre UTC para evitar que el token expire antes de tiempo
        expire = datetime.now(timezone.utc) + timedelta(minutes=DURATION)
        data_copy["exp"] = expire
        payload = jwt.encode(data_copy, KEY_SECRET, algorithm=ALGORITH)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error al generar el token"
        )

def get_current_user(token: str = Depends(oauth2)):
    try:
        payload = jwt.decode(token, KEY_SECRET, algorithms=[ALGORITH])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
                )
        
        # Buscamos solo los campos necesarios
        user = db_client.user.find_one({"username": username})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        return UserOut(**user)
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")
    
