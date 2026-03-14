
from fastapi import FastAPI
from schemas.schemes import Movie
from router import users, sign_up
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(users.router)
app.include_router(sign_up.router)

@app.get("/")
async def hi():
    return "Bienvenido a ver pelicualas"


# Esto va justo después de crear la variable 'app = FastAPI()'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción pondrías tu dominio real
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn main:app --reload

