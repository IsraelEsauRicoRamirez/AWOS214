
from typing import Optional
import asyncio
from app.data.database import usuarios
from fastapi import APIRouter

router = APIRouter(tags=['Varios'])

#Endpoints varios
@router.get("/")
async def bienvenida():
    return{"mensaje": "¡Bienvenido a mi API!"}

@router.get("/HolaMundo")
async def Hola():
    await asyncio.sleep(4)#Simulación de petición
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus":"200"
           
           }
#API con parametro Obligatorio
@router.get("/v1/parametroOb/{id}")
async def consultaUno(id:int):
    return{"Se encontro usuario": id}

#API con parametro Opcional
@router.get("/v1/parametroOp/")
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje": "Usuario encontrado", "usuario":usuario}
        return{"mensaje": "Usuario no encontrado", "usuario":id}
    else:
        return{"mensaje": "No se proporciono id"}
            
