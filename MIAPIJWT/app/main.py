#Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta



#Instancia del servidor
app = FastAPI(
    title='Mi Segunda API YUPIII :)',
    description='Israel Esau Rico Ramirez',
    version='1.0.0'
    )

# Configuración de seguridad JWT
SECRET_KEY = "Noledigasanadiemiclave"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Indica que el token será tipo Bearer y que se generará en token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#Función para crear el token 
def crear_token(data: dict):
    to_encode = data.copy()

    # Crear fecha de expiración
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Agregar expiración al token
    to_encode.update({"exp": expire})

    # Generar token firmado
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#Validaar token
def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decodificar token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Extraer usuario
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

#TB ficticia
usuarios=[
    {"id":1, "nombre":"Juan", "edad":21},
    {"id":2, "nombre":"Israel", "edad":21},
    {"id":3, "nombre":"Sofi", "edad":21}
 
]

#Modelo de validacion Pydantic
class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre:str = Field(...,min_length=3, max_length=50, example="Juanita" )
    edad: int  = Field(...,ge=1, le=123, description= "Edad valida entre 1 y 123")


#Modelo de validacion de Pydantic para eliminar
class usuario_delete(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
   




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
            
#Enndpoint para generar token
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    
    # Validación simple (como tenías en HTTP Basic)
    if form_data.username != "israelesau" or form_data.password != "123456":
        raise HTTPException(
            status_code=400,
            detail="Credenciales incorrectas"
        )

    # Crear token
    access_token = crear_token(data={"sub": form_data.username})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


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
async def crear_usuarios(usuario:usuario_create):
    for usr in usuarios:
        if usr["id"] == usuario.id:
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
async def actualizar_usuarios(id:int , usuario:dict,user:str = Depends(validar_token)):
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
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuarios(id:int, user:str = Depends(validar_token)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return{
                "mensaje": f"Usuario Eliminado por  {user} ",
                
            }
    raise HTTPException (
                status_code=400,
                detail="El id no existe"
            )