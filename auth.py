from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.user import User
from app.schemas.auth_schema import SignupRequest, LoginRequest
from app.auth.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(payload: SignupRequest):
    db = SessionLocal()

    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password)
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "Signup successful"}

@router.post("/login")
def login(payload: LoginRequest):
    db = SessionLocal()
    user = db.query(User).filter(User.email == payload.email).first()
    db.close()

    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token}
