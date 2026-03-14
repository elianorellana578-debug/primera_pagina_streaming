
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # <--- NUEVO
from router import users, sign_up
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(sign_up.router)

# CAMBIO AQUÍ: En lugar de devolver un texto, devolvemos el archivo index.html
@app.get("/", response_class=HTMLResponse)
async def hi():
    # Buscamos el archivo index.html en tu carpeta principal
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "API Online - Pero no se encontró el archivo index.html en la raíz del proyecto"

