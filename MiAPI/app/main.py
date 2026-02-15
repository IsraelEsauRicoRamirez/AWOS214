#Importaciones
from fastapi import FastAPI, status, HTTPException
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
@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return{"Se encontro usuario": id}

#API con parametro Opcional
@app.get("/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultaTodos(id:Optional[int]=None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return{"mensaje": "Usuario encontrado", "usuario":usuario}
        return{"mensaje": "Usuario no encontrado", "usuario":id}
    else:
        return{"mensaje": "No se proporciono id"}
            

#Endpoint donde utiliza el GET 

@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
    }

#Endpoint para post, nota: Si pueden tener el mismo nombre mientras sean diferentes, si son dos get ahi no.
@app.post("/v1/usuarios/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def crear_usuarios(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException (
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)#append es el insert a mi tabla ficticia 
    return{
        "mensaje":"Uusario Agregado",
        "Usuario":usuario
    }

#Endpoint para Put(Actualizar)
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def actualizar_usuarios(id:int , usuario:dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return{
                "mensaje":"Usuario Actualizado",
                "Usuario":usr
            }
    raise HTTPException (
                status_code=400,
                detail="El id no existe"
            )
            
  
#Endpoint para Delete(Eliminar)
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuarios(id:int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "mensaje":"Usuario Eliminado",
                
            }
    raise HTTPException (
                status_code=400,
                detail="El id no existe"
            )