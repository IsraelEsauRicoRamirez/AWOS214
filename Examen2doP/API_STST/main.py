#Importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, EmailStr
from datetime import datetime
from datetime import date


#Instancia del servidor
app = FastAPI(
    title='API REPASO :)',
    description='Israel Esau Rico Ramirez',
    version='1.0.0'
    )


#Endpoints
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return{"mensaje": "¡Bienvenido a la API de la Biblioteca digital "}

#--------------------------------------- Validaciones------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Modelo de validacion Pydantic
class libro_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(...,min_length=2, max_length=100, example="Cien años de soledad" )
    paginas: int  = Field(...,gt=1, description= "Numero de paginas validas mayor a 1")
    anio_publicacion: int = Field(..., gt=1450, description="Año mayor a 1450")
    estado: Literal["disponible", "prestado"]
    @field_validator('anio_publicacion')
    def validar_anio_actual(cls, a):
        anio_actual = datetime.now().year
        if a > anio_actual:
            raise ValueError(f'El año no puede ser mayor al actual ({anio_actual})')
        return a
class usuario_create(BaseModel):
    id: int = Field(..., gt=0, description="Identificador único del usuario")
    nombre: str = Field(..., min_length=2, max_length=100, example="Fidel")
    correo: EmailStr = Field(..., example="Fidel@gmail.com")


class prestamo_create(BaseModel):
    id: int = Field(..., gt=0, description="ID único del préstamo")
    libro_id: int = Field(..., gt=0, description="ID del libro a prestar")
    usuario_id: int = Field(..., gt=0, description="ID del usuario que recibe el libro")
    fecha_prestamo: str = Field(default=str(date.today()), description="Fecha en formato YYYY-MM-DD")
   
#--------------------------------------- Tablas----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------Usuarios---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
usuarios=[
    {"id":1, "nombre":"Fidel", "correo":"Fidel@gmail.com"},
    {"id":2, "nombre":"Yael", "correo":"Yael@gmail.com"},
    {"id":3, "nombre":"Abdiel", "correo":"Abdiel@gmail.com"}
 
]
#-------------------------Libros---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

libros = [
    {
        "id": 1, "nombre": "Cien años de soledad", "autor": "Gabriel García Márquez", "anio_publicacion": 1967, "paginas": 417, "estado": "disponible"
    },
    {
        "id": 2, "nombre": "Comeras flores",  "autor": "Lucía Solla Sobral", "anio_publicacion":  2025, "paginas": 248, "estado": "prestado"  
    },
    {
        "id": 3, "nombre": "Hábitos atómicos",  "autor": "James Clear", "anio_publicacion": 2018, "paginas": 328 , "estado": "disponible"
    },
    
]
#-------------------------Prestamos------------------------------------------------------------------------------------------------------------
prestamos = [
    {
        "id": 1, "libro_id": 2, "usuario_id": 1, "fecha_prestamo": "2023-10-25" 
    }
]

#--------------------------------------- EndPoints-------------------------------------------------------------------------------------------------------

@app.post("/v1/biblioteca/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def registrar_libro(libro:libro_create):
    for lbr in libros:
        if lbr["id"] == libro.id:
            raise HTTPException (
                status_code=400,
                detail="El id ya existe"
            )
    libros.append(libro)#append es el insert a mi tabla ficticia 
    return{
        "mensaje":"Libro agregado",
        "Libro":libro
    }
    
@app.get("/v1/biblioteca/", tags=['CRUD HTTP'])
async def leer_Libros():
    return{
        "status":"200",
        "total": len(libros),
        "libros":libros
    }

@app.get("/v1/biblioteca/{nombre}", tags=['CRUD HTTP'])
async def consultalibros(nombre:str):
    if nombre is not None:
        for libro in libros:
            if libro["nombre"] == nombre:
                return{"mensaje": "Libro encontrado", "libro":libro}
        return{"mensaje": "Libro no encontrado", "libro":nombre}
    else:
        return{"mensaje": "No se proporciono nombre"}
    
@app.post("/v2/biblioteca/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def registrar_prestamo(prestamo: prestamo_create): 
    
  
    for pre in prestamos:
        if pre["id"] == prestamo.id:
            raise HTTPException(status_code=400, detail="El ID del préstamo ya existe")

   
    usuario_existe = False
    for usu in usuarios:
        if usu["id"] == prestamo.usuario_id:
            usuario_existe = True
            break
    if not usuario_existe:
        raise HTTPException(status_code=404, detail="El usuario no existe")

   
    libro_encontrado = None
    for lib in libros:
        if lib["id"] == prestamo.libro_id:
            libro_encontrado = lib
            break
            
    if not libro_encontrado:
        raise HTTPException(status_code=404, detail="El libro no existe")

   
    if libro_encontrado["estado"] == "prestado":
        raise HTTPException(
            status_code=409, 
            detail=f"El libro '{libro_encontrado['nombre']}' ya está prestado y no se puede generar su prestamo."
        )

  

    
    libro_encontrado["estado"] = "prestado" 


    prestamos.append(prestamo.model_dump()) 

    return {
        "mensaje": "Préstamo ",
        "libro_actualizado": libro_encontrado, 
        "Prestamo": prestamo
    }


@app.put("/v1/biblioteca/{libro_id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def devolver_libro(libro_id: int):
    libro_encontrado = False
    
    for lbr in libros:
        if lbr["id"] == libro_id:
            libro_encontrado = True
            
            
            if lbr["estado"] == "disponible":
                raise HTTPException(
                    status_code=409,
                    detail=" El libro ya está disponible"
                )
            
            
            lbr["estado"] = "disponible"
            
            return {
                "mensaje": f"El libro '{lbr['nombre']}' se ha devuelto a la biblioteca",
                "libro": lbr
            }

    
    if libro_encontrado == False:
        raise HTTPException(
            status_code=404, 
            detail="El libro no existe"
        )
    

@app.delete("/v1/biblioteca/{id_prestamo}", tags=['CRUD HTTP'])
async def eliminar_prestamo(id_prestamo: int):
    
    for prestamo in prestamos:
        if prestamo["id"] == id_prestamo:
            
            id_libro_a_liberar = prestamo["libro_id"]

            for libro in libros:
                if libro["id"] == id_libro_a_liberar:
                    libro["estado"] = "disponible"
                    break 
                
            prestamos.remove(prestamo)
            
            return {
                "mensaje": "Préstamo eliminado",
                "id_prestamo": id_prestamo,
                
            }
    
    raise HTTPException(
        status_code=404, 
        detail="El préstamo no existe"
    )