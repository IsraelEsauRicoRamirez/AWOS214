#Importaciones
from fastapi import FastAPI
import asyncio

#Instancia del servidor
app = FastAPI()

#Endpoints
@app.get("/")
async def bienvenida():
    return{"mensaje": "¡Bienvenido a mi API!"}

@app.get("/HolaMundo")
async def bienvenida():
    await asyncio.sleep(4)#Simulación de petición
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus":"200"
           
           }