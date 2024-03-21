from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256

app = FastAPI()
security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = security):
    correct_username = "test"
    correct_password = "123456"

    hashed_password = sha256(correct_password.encode()).hexdigest()

    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    security_scopes = ["basic"]
    try:
        security_scopes, user = authenticate_user(request)
    except:
        raise HTTPException(status_code=401, detail="Unauthorized")

    response = await call_next(request)
    return response

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI with Middleware Authorization"}