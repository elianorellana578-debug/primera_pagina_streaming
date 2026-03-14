
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import users, sign_up

app = FastAPI()

# EL CAMBIO: Configuración de CORS al principio para que Render no bloquee el Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite que tu dominio de Render se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(sign_up.router)

@app.get("/")
async def hi():
    return {"message": "Bienvenido a la API de Películas - Activa y Desplegada"}

# El comando en Render debe ser: uvicorn main:app --host 0.0.0.0 --port $PORT

