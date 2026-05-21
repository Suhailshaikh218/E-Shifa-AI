"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from databases import Database
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, get_current_user
from app.schemas.auth import SignUpSchema, LoginSchema, TokenResponse, UserResponse
import uuid

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: SignUpSchema, db: Database = Depends(get_db)):
    """
    Register a new user account
    
    Supports all 6 roles: system_owner, patient, nurse_provider, 
    dispenser_provider, hospital_admin, pharmacy_admin
    """
    
    # Check if phone number already exists
    existing_user = await db.fetch_one(
        "SELECT id FROM users_auth WHERE phone_number = :phone",
        {"phone": user.phone_number}
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Check if email already exists (if provided)
    if user.email:
        existing_email = await db.fetch_one(
            "SELECT id FROM users_auth WHERE email = :email",
            {"email": user.email}
        )
        
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Hash password
    hashed_password = hash_password(user.password)
    
    # Insert new user
    user_id = str(uuid.uuid4())
    
    query = """
        INSERT INTO users_auth (id, full_name, phone_number, email, password_hash, role, is_active)
        VALUES (:id, :full_name, :phone_number, :email, :password_hash, :role, :is_active)
        RETURNING id, full_name, role
    """
    
    values = {
        "id": user_id,
        "full_name": user.full_name,
        "phone_number": user.phone_number,
        "email": user.email,
        "password_hash": hashed_password,
        "role": user.role,
        "is_active": True
    }
    
    new_user = await db.fetch_one(query, values)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_user["id"]), "role": new_user["role"]}
    )
    
    print(f"[AUTH TRACE]: New Account Registered - {user.full_name} as {user.role}")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(new_user["id"]),
        role=new_user["role"],
        full_name=new_user["full_name"]
    )


@router.post("/login", response_model=TokenResponse)
async def login_user(credentials: LoginSchema, db: Database = Depends(get_db)):
    """
    Authenticate user and return JWT token
    """
    
    # Fetch user by phone number
    query = """
        SELECT id, full_name, password_hash, role, is_active
        FROM users_auth
        WHERE phone_number = :phone
    """
    
    user = await db.fetch_one(query, {"phone": credentials.phone_number})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password"
        )
    
    # Check if account is active
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user["id"]), "role": user["role"]}
    )
    
    print(f"[AUTH TRACE]: User Login - {user['full_name']} ({user['role']})")
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user["id"]),
        role=user["role"],
        full_name=user["full_name"]
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Database = Depends(get_db)
):
    """
    Get current authenticated user information
    """
    query = """
        SELECT id, full_name, phone_number, email, role, is_active, created_at
        FROM users_auth
        WHERE id = :user_id
    """
    
    user = await db.fetch_one(query, {"user_id": current_user["user_id"]})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(**dict(user))
