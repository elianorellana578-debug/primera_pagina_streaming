
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # <--- ASEGÚRATE DE TENER ESTO
from router import users, sign_up
import os # <--- Y ESTO TAMBIÉN

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

@app.get("/", response_class=HTMLResponse)
async def hi():
    # Buscamos el archivo dentro de tu carpeta 'html'
    ruta_html = os.path.join("html", "index.html")
    
    if os.path.exists(ruta_html):
        with open(ruta_html, "r", encoding="utf-8") as f:
            return f.read()
    
    return f"Error: No encontré el archivo en la ruta: {ruta_html}. Revisa que la carpeta se llame 'html' (en minúsculas)."

