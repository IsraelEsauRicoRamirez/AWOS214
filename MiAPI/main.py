#Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

#Instancia del servidor
app = FastAPI(
    title='Mi primer API YUPIII :)',
    description='Israel Esau Rico Ramirez',
    version='1.0.0'
    )
#TB ficticia
usuarios=[
    {"id":1, "nombre":"Juan", "edad":21},
    {"id":2, "nombre":"Israel", "edad":21},
    {"id":3, "nombre":"Sofi", "edad":21}
    

]

#Endpoints
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return{"mensaje": "¡Bienvenido a mi API!"}

@app.get("/HolaMundo",tags=['Bienvenida Asincrona'])
async def Hola():
    await asyncio.sleep(4)#Simulación de petición
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus":"200"
           
           }
#API con parametro Obligatorio
@app.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return{"Se encontro usuario": id}

#API con parametro Opcional
@app.get("/v1/usuario/", tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje": "Usuario encontrado", "usuario":usuario}
        return{"mensaje": "Usuario no encontrado", "usuario":id}
    else:
        return{"mensaje": "No se proporciono id"}
            