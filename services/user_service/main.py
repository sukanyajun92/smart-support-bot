from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from user_service import schemas
from user_service.auth import verify_password, get_password_hash, create_access_token
from user_service.dependencies import get_db, get_current_user
from user_service.models import UserDB
from datetime import timedelta
from sqlalchemy.exc import IntegrityError

app = FastAPI()

@app.post("/signup", response_model=schemas.User)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = get_password_hash(user.password)
    db_user = UserDB(
        email=user.email,
        name=user.name,
        hashed_password=hashed_pw
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.User)
def get_me(current_user: UserDB = Depends(get_current_user)):
    return current_user