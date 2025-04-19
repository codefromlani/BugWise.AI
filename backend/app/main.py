from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.api.v1.routes import user
from app.api.v1.schemas.user import Token
from app.api.core.security import get_user, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from app.api.db.database import get_db
from datetime import timedelta

from app.api.v1.routes import bugs

app = FastAPI(
    title= "BugWise AI"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8080"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(bugs.router, prefix="/api/v1")
app.include_router(user.user_router, prefix="/api/v1")

@app.get("/")
def home():
    return {"message": "Welcome to BugWise AI!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}