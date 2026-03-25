#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

from app.data.db import engine
from app.data import usuario  

#Crear un ojeto justo como me lo dice mi modelo 
usuario.Base.metadata.create_all(bind=engine)

#Instancia del servidor
app = FastAPI(
    title='Mi primer API YUPIII :)',
    description='Israel Esau Rico Ramirez',
    version='1.0.0'
    )


app.include_router(usuarios.router)
app.include_router(varios.router)