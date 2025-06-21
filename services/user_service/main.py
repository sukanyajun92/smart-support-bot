# user_service/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from user_service import models, schemas
from user_service.auth import verify_password, get_password_hash, create_access_token
from user_service.dependencies import get_db, get_current_user, engine
from user_service.models import UserDB, Base
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
import random

app = FastAPI()

# 🛠️ Create tables on app startup
Base.metadata.create_all(bind=engine)

# 🔧 Seed 10 users if table is empty
def seed_users():
    from user_service.dependencies import SessionLocal
    db = SessionLocal()
    try:
        if db.query(UserDB).count() == 0:
            for i in range(1, 11):
                email = f"user{i}@example.com"
                user = UserDB(
                    email=email,
                    name=f"User {i}",
                    hashed_password=get_password_hash("password123"),
                    preferences="chat,genAI" if i % 2 == 0 else "cloud,backend"
                )
                db.add(user)
            db.commit()
            print("✅ Seeded 10 users")
    finally:
        db.close()

seed_users()

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

@app.get("/users", response_model=list[schemas.User])
def list_users(db: Session = Depends(get_db)):
    users = db.query(UserDB).all()
    return users
