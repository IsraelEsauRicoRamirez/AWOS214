from fastapi import FastAPI, status, HTTPException, Depends

from typing import Literal
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
#Instancia del servidor
app = FastAPI(
    title='API Sistema de Tickets de Soporte Técnico',
    description='Israel Esau Rico Ramirez',
    version='1.0.0'
    )

#Seguridad HTTP Basic

security=HTTPBasic()

def Verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "soporte")
    passAuth = secrets.compare_digest(credenciales.password, "4321")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= " Credenciales no Autorizadas"
        )
    return credenciales.username
#Endpoints
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return{"mensaje": "¡Bienvenido a la API de sistema de Tickets digital "}

#--------------------------------------- Validaciones------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Modelo de validacion Pydantic
class ticket_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre_usuario: str = Field(...,gt=5 , example="Abdiel Gonzales Paulin" )
    Descripción_problema: str = Field(...,min_length=20 , max_length=200, description= "La pagina dejo de Funcionar al camiar el estilo de la misma paginaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    prioridad: Literal["Baja","Media","Alta"]
    estado: Literal["Pendiente", "Resuelto"]
   




   
#--------------------------------------- Tablas----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#-------------------------Tickets---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

tickets = [
    {
        "id": 1, "nombre_usuario": "Israel Esau Rico Ramirez", "Descripción_problema": "La app dejo de funcionar al intertar implementar la base de datos", "prioridad": "Baja","estado": "Pendiente"
    },
    {
        "id": 2, "nombre_usuario": "Juan Fidel Juarez Torres", "Descripción_problema": "Al intentar probar el sistema lanzo un errror de código que necesita checarse", "prioridad": "Media","estado": "Pendiente"
    },
    {
        "id": 3, "nombre_usuario": "Yael Alejandro Urbano Zuñiga", "Descripción_problema": "La aplicacion no maneja base de datos al interntar probarla de manera usual", "prioridad": "Alta","estado": "Resuelto"
    },
    
]

#--------------------------------------- EndPoints-------------------------------------------------------------------------------------------------------


#Listar Tickets
@app.get("/v1/STicketsST/", tags=['CRUD HTTP'])
async def leer_tickets():
    return{
        "status":"200",
        "total": len(tickets),
        "libros":tickets
    }
#Crear Tickets
@app.post("/v1/STicketsST/", tags=['CRUD HTTP'], status_code=status.HTTP_201_CREATED)
async def registrar_ticket(Ticket:ticket_create):
    for tckt in tickets:
        if tckt["id"] == Ticket.id:
            raise HTTPException (
                status_code=400,
                detail="El id ya existe"
            )
    tickets.append(Ticket)
    return{
        "mensaje":"Ticket agregado",
        "Ticket":Ticket
    }
#Consultar Tickets por id 
@app.get("/v1/STicketsST/{id}", tags=['CRUD HTTP'])
async def consultalibros(id:int, userAuth:str= Depends(Verificar_Peticion)):
    if id is not None:
        for Ticket in tickets:
            if Ticket["id"] == id:
                return{"mensaje": "Ticket encontrado", "Ticket Encontrado":Ticket}
        return{"mensaje": "Ticket no encontrado", "Ticket":id}
    else:
        return{"mensaje": "No se proporciono un id"}
    



@app.put("/v1/STicketsST/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def cambiar_estado_ticket(id: int):
    Ticket_encontrado = False
    
    for tcket in tickets:
        if tcket["id"] == id:
            Ticket_encontrado= True
            
            
            if tcket["estado"] == "Resuelto":
                raise HTTPException(
                    status_code=409,
                    detail=" El Ticket ya fue Resuelto"
                )
            
            
            tcket["estado"] = "Resuelto"
            
            return {
                "mensaje": f"El libro '{tcket['id']}' se ha Resuelto Corectamente",
                "Ticket": tcket
            }

    
    if Ticket_encontrado == False:
        raise HTTPException(
            status_code=404, 
            detail="El Ticket no existe"
        )
    
@app.delete("/v1/STicketsST/{id}", tags=['CRUD HTTP'])
async def eliminar_prestamo(id: int):
    
    for ticket in tickets:
        if ticket["id"] == id:
            tickets.remove(ticket)
      
            
            return {
                "mensaje": "Préstamo eliminado",
                "id_Ticket": id,
                
            }
    
    raise HTTPException(
        status_code=404, 
        detail="El Ticket no existe"
    )
