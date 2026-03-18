
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fastapi import  HTTPException, Depends, status
#Seguridad HTTP Basic

security=HTTPBasic()

def Verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "israelesau")
    passAuth = secrets.compare_digest(credenciales.password, "123456")

    if not(userAuth and passAuth):
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= " Credenciales no Autorizadas"
        )
    return credenciales.username