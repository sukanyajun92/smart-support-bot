from sqlalchemy.orm import Session
from user_service import models, schemas
from user_service.auth import get_password_hash
from sqlalchemy.exc import IntegrityError

# Create new user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.UserDB(
        email=user.email,
        name=user.name,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.UserDB).filter(models.UserDB.email == email).first()

# Update user's last login
def update_last_login(db: Session, user: models.UserDB):
    user.last_login = models.datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user
