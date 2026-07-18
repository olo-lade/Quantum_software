# Original Author: Joshua Tosin Pamilerin (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

import os
import json
import secrets
from datetime import datetime
from collections import defaultdict
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from app.database import engine, get_db, Base
from app import models
from app.quantum_logic.cryptography import generate_quantum_key
from app.quantum_logic.logistics import optimize_route
from app.quantum_logic.finance import optimize_portfolio

load_dotenv()

# ---------------------------------------------------------------------------
# Startup: create tables
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Universal Quantum API",
    description="Quantum-as-a-Service (QaaS) abstraction layer.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# In-memory rate limiter: max 10 requests / minute per API key
# ---------------------------------------------------------------------------

_rate_store: dict[str, list[datetime]] = defaultdict(list)
RATE_LIMIT = 10
RATE_WINDOW = 60  # seconds


def _check_rate_limit(api_key: str):
    now = datetime.utcnow()
    window = _rate_store[api_key]
    _rate_store[api_key] = [t for t in window if (now - t).seconds < RATE_WINDOW]
    if len(_rate_store[api_key]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Max 10 requests/minute.")
    _rate_store[api_key].append(now)


# ---------------------------------------------------------------------------
# Auth dependency
# ---------------------------------------------------------------------------

def authenticate(x_api_key: str = Header(...), db: Session = Depends(get_db)) -> models.APIKey:
    record = db.query(models.APIKey).filter(models.APIKey.key == x_api_key).first()
    if not record:
        raise HTTPException(status_code=401, detail="Invalid API key.")
    _check_rate_limit(x_api_key)
    return record


# ---------------------------------------------------------------------------
# Logging helper
# ---------------------------------------------------------------------------

def log_job(db: Session, user_id: str, endpoint: str, input_data: dict, result: dict):
    db.add(models.JobLog(
        user_id=user_id,
        endpoint=endpoint,
        input_data=json.dumps(input_data),
        result=json.dumps(result),
    ))
    db.commit()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class KeyGenRequest(BaseModel):
    num_bits: int = Field(default=256, ge=8, le=512, description="Key length in bits (multiples of 8).")

class RouteRequest(BaseModel):
    distances: list[list[float]] = Field(..., description="NxN distance matrix between cities.")

class PortfolioRequest(BaseModel):
    returns: list[float] = Field(..., description="Expected return per asset.")
    risk_matrix: list[list[float]] = Field(..., description="NxN covariance/risk matrix.")
    risk_tolerance: float = Field(default=0.5, ge=0.0, le=1.0)


# ---------------------------------------------------------------------------
# User & API Key management
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    email: str

@app.post("/users", tags=["Admin"], summary="Register a new user and receive an API key.")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered.")
    user = models.User(email=payload.email)
    db.add(user)
    db.flush()
    api_key = models.APIKey(key=secrets.token_hex(32), user_id=user.id)
    db.add(api_key)
    db.commit()
    return {"user_id": user.id, "api_key": api_key.key}


# ---------------------------------------------------------------------------
# Quantum endpoints
# ---------------------------------------------------------------------------

@app.post("/quantum/crypto/keygen", tags=["Cryptography"], summary="Generate a quantum-random cryptographic key.")
def keygen(payload: KeyGenRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    result = {"key": generate_quantum_key(payload.num_bits), "bits": payload.num_bits}
    log_job(db, auth.user_id, "/quantum/crypto/keygen", payload.model_dump(), result)
    return result


@app.post("/quantum/logistics/optimize", tags=["Logistics"], summary="Optimize a multi-city route via QAOA.")
def route_optimize(payload: RouteRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    n = len(payload.distances)
    if any(len(row) != n for row in payload.distances):
        raise HTTPException(status_code=422, detail="distances must be a square NxN matrix.")
    result = optimize_route(payload.distances)
    log_job(db, auth.user_id, "/quantum/logistics/optimize", payload.model_dump(), result)
    return result


@app.post("/quantum/finance/portfolio", tags=["Finance"], summary="Quantum portfolio optimization via VQE ansatz.")
def portfolio(payload: PortfolioRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    n = len(payload.returns)
    if len(payload.risk_matrix) != n or any(len(r) != n for r in payload.risk_matrix):
        raise HTTPException(status_code=422, detail="risk_matrix must be NxN matching the number of assets.")
    result = optimize_portfolio(payload.returns, payload.risk_matrix, payload.risk_tolerance)
    log_job(db, auth.user_id, "/quantum/finance/portfolio", payload.model_dump(), result)
    return result


@app.get("/health", tags=["System"], summary="Health check.")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}
