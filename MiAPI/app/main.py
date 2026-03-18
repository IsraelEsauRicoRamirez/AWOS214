#Importaciones
from fastapi import FastAPI
from app.routers import usuarios, varios

#Instancia del servidor
app = FastAPI(
    title='Mi primer API YUPIII :)',
    description='Israel Esau Rico Ramirez',
    version='1.0.0'
    )


app.include_router(usuarios.router)
app.include_router(varios.router)