from fastapi import FastAPI, Depends, HTTPException, Header, status, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database import init_db, get_db
from models import User, Session as SessionModel
from schemas import RegisterRequest, LoginRequest, TokenResponse, UserInfo, APIResponse
from auth import hash_password, verify_password, create_access_token, verify_token, RATE_LIMIT_CALLS_PER_DAY
from asr import transcribe
from llm import generate_reply

app = FastAPI(title="Voice Medical AI Assistant API")
init_db()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RECORDINGS_DIR = Path(__file__).parent / "recordings"


def _create_session(user_id: int, db: Session) -> TokenResponse:
    token, expires_at = create_access_token(user_id)
    db.add(SessionModel(user_id=user_id, token=token, expires_at=expires_at))
    db.commit()
    return TokenResponse(access_token=token, expires_at=expires_at)


def _enforce_rate_limit(session: SessionModel) -> None:
    if session.api_calls_today >= RATE_LIMIT_CALLS_PER_DAY:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Daily API limit ({RATE_LIMIT_CALLS_PER_DAY}) exceeded",
        )


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == req.email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already registered")

    user = User(username=req.username, email=req.email, hashed_password=hash_password(req.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return _create_session(user.id, db)


@app.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    return _create_session(user.id, db)


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
) -> tuple[User, SessionModel]:
    if not authorization:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing authorization header")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid authorization header")

    token = parts[1]
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    session = db.query(SessionModel).filter(
        SessionModel.token == token,
        SessionModel.is_active == True,
    ).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Session expired")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user, session


@app.get("/user/profile", response_model=UserInfo)
def get_profile(current: tuple = Depends(get_current_user)):
    user, session = current
    return UserInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at,
        api_calls_today=session.api_calls_today,
    )


@app.post("/auth/logout", response_model=APIResponse)
def logout(current: tuple = Depends(get_current_user), db: Session = Depends(get_db)):
    _, session = current
    session.is_active = False
    db.commit()
    return APIResponse(success=True, message="Logged out successfully")


@app.get("/api/protected-endpoint", response_model=APIResponse)
@limiter.limit("100/minute")
def protected_endpoint(
    request: Request,
    current: tuple = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    _, session = current
    _enforce_rate_limit(session)
    session.api_calls_today += 1
    db.commit()
    return APIResponse(
        success=True,
        message="Request successful",
        data={"calls_remaining": RATE_LIMIT_CALLS_PER_DAY - session.api_calls_today},
    )


@app.post("/api/voice", response_model=APIResponse)
@limiter.limit("60/minute")
async def upload_voice(
    request: Request,
    audio: UploadFile = File(...),
    current: tuple = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> APIResponse:
    user, session = current
    _enforce_rate_limit(session)

    RECORDINGS_DIR.mkdir(exist_ok=True)
    filename = f"user_{user.id}_{int(datetime.utcnow().timestamp())}_{audio.filename}"
    contents = await audio.read()
    (RECORDINGS_DIR / filename).write_bytes(contents)

    transcript = await transcribe(contents, filename)
    reply = generate_reply(transcript)

    session.api_calls_today += 1
    db.commit()

    return APIResponse(
        success=True,
        message="Audio received",
        data={
            "filename": filename,
            "transcript": transcript,
            "reply": reply.get("reply", ""),
            "signal": reply.get("signal", "watch"),
            "title": reply.get("title", ""),
            "calls_remaining": RATE_LIMIT_CALLS_PER_DAY - session.api_calls_today,
        },
    )
