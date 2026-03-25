
from fastapi import status , HTTPException, Depends, APIRouter
from app.models.usuario import usuario_create
from app.data.database import usuarios
from app.security.auth import Verificar_Peticion


from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB



router = APIRouter(
    prefix= "/v1/usuarios", tags=['CRUD HTTP']
)



# ---------- Endpoints Usuarios --------------- 
#Endpoint donde utiliza el GET 

@router.get("/")
async def leer_usuarios(db:Session= Depends(get_db)): #Si hay una sesion y hay forma de conectarse muestra si no no va a poder hacerlo 
    queryUsers= db.query(usuarioDB).all() #Basicamente es un Select usuarios en sql en python
    return{
        "status":"200",
        "total": len(queryUsers),
        "usuarios":queryUsers
    }

#Endpoint para post, nota: Si pueden tener el mismo nombre mientras sean diferentes, si son dos get ahi no.
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuarios(usuarioP:usuario_create, db:Session= Depends(get_db)):
    
    nuevoUsuario= usuarioDB(nombre= usuarioP.nombre, edad= usuarioP.edad)
    db.add(nuevoUsuario)
    db.commit()#Confirmamos
    db.refresh(nuevoUsuario)#Actualizamos

    return{
        "mensaje":"Uusario Agregado",
        "Usuario": usuarioP
    }

#Endpoint para Put(Actualizar)
@router.put("/{id}", status_code=status.HTTP_200_OK)
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
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuarios(id:int, userAuth:str= Depends(Verificar_Peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "mensaje": f"Usuario Eliminado por {userAuth}",
                
            }
    raise HTTPException (
                status_code=400,
                detail="El id no existe"
            )