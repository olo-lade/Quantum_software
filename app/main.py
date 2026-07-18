# Original Author: Oluwatosin Olalere (GitHub: olo-lade)
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
from app.quantum_logic.cryptography import (
    generate_quantum_key, score_entropy, quantum_otp_encrypt,
    quantum_otp_decrypt, simulate_bb84
)
from app.quantum_logic.key_management import (
    issue_key, rotate_key, revoke_key, verify_managed_key,
    get_audit_logs, get_threat_events, resolve_threat
)
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

class EntropyRequest(BaseModel):
    num_bits: int = Field(default=64, ge=8, le=128)
    shots: int = Field(default=1024, ge=64, le=4096)

class OTPEncryptRequest(BaseModel):
    plaintext: str = Field(..., min_length=1, max_length=256)

class OTPDecryptRequest(BaseModel):
    ciphertext: str
    key: str

class BB84Request(BaseModel):
    num_bits: int = Field(default=16, ge=8, le=64)

# Key Management
class KeyIssueRequest(BaseModel):
    app_id: str = Field(..., min_length=1, max_length=100)
    key_bits: int = Field(default=256, ge=128, le=512)
    ttl_hours: int | None = Field(default=None, ge=1, le=8760)

class KeyVerifyRequest(BaseModel):
    key_id: str
    key_value: str

class AuditQueryRequest(BaseModel):
    app_id: str | None = None
    limit: int = Field(default=50, ge=1, le=200)

class ThreatQueryRequest(BaseModel):
    app_id: str | None = None
    unresolved_only: bool = True


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


@app.post("/quantum/crypto/entropy", tags=["Cryptography"], summary="Score quantum randomness quality via Shannon entropy.")
def entropy(payload: EntropyRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    result = score_entropy(payload.num_bits, payload.shots)
    log_job(db, auth.user_id, "/quantum/crypto/entropy", payload.model_dump(), result)
    return result


@app.post("/quantum/crypto/otp/encrypt", tags=["Cryptography"], summary="Encrypt a message using a quantum One-Time Pad.")
def otp_encrypt(payload: OTPEncryptRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    result = quantum_otp_encrypt(payload.plaintext)
    log_job(db, auth.user_id, "/quantum/crypto/otp/encrypt", {"message_length": len(payload.plaintext)}, result)
    return result


@app.post("/quantum/crypto/otp/decrypt", tags=["Cryptography"], summary="Decrypt a quantum One-Time Pad ciphertext.")
def otp_decrypt(payload: OTPDecryptRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        result = quantum_otp_decrypt(payload.ciphertext, payload.key)
    except (ValueError, UnicodeDecodeError) as e:
        raise HTTPException(status_code=422, detail=str(e))
    log_job(db, auth.user_id, "/quantum/crypto/otp/decrypt", {}, result)
    return result


@app.post("/quantum/crypto/bb84", tags=["Cryptography"], summary="Simulate BB84 Quantum Key Distribution with eavesdropping detection.")
def bb84(payload: BB84Request, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    result = simulate_bb84(payload.num_bits)
    log_job(db, auth.user_id, "/quantum/crypto/bb84", payload.model_dump(), result)
    return result


@app.get("/health", tags=["System"], summary="Health check.")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


# ---------------------------------------------------------------------------
# Key Management endpoints
# ---------------------------------------------------------------------------

@app.post("/quantum/keys/issue", tags=["Key Management"], summary="Issue a quantum-random key for a client app.")
def keys_issue(payload: KeyIssueRequest, request: Request, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    record = issue_key(db, auth.user_id, payload.app_id, payload.key_bits, payload.ttl_hours)
    return {
        "key_id": record.id,
        "app_id": record.app_id,
        "key_value": record.key_value,
        "key_bits": record.key_bits,
        "status": record.status,
        "expires_at": record.expires_at.isoformat() if record.expires_at else None,
    }


@app.post("/quantum/keys/{key_id}/rotate", tags=["Key Management"], summary="Rotate an existing managed key.")
def keys_rotate(key_id: str, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        record = rotate_key(db, key_id, auth.user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {
        "key_id": record.id,
        "key_value": record.key_value,
        "status": record.status,
        "previous_key": record.previous_key,
    }


@app.delete("/quantum/keys/{key_id}/revoke", tags=["Key Management"], summary="Revoke a managed key permanently.")
def keys_revoke(key_id: str, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        return revoke_key(db, key_id, auth.user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/quantum/keys/verify", tags=["Key Management"], summary="Verify a managed key with threat detection.")
def keys_verify(payload: KeyVerifyRequest, request: Request, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    ip = request.client.host if request.client else None
    return verify_managed_key(db, payload.key_id, payload.key_value, ip)


# ---------------------------------------------------------------------------
# Audit & Threat Monitoring endpoints
# ---------------------------------------------------------------------------

@app.post("/quantum/audit/query", tags=["Audit"], summary="Query tamper-evident audit logs for your apps.")
def audit_query(payload: AuditQueryRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    logs = get_audit_logs(db, auth.user_id, payload.app_id, payload.limit)
    return [{"id": l.id, "app_id": l.app_id, "event_type": l.event_type,
             "detail": l.detail, "ip_address": l.ip_address,
             "created_at": l.created_at.isoformat()} for l in logs]


@app.post("/quantum/monitor/alerts", tags=["Monitoring"], summary="Get active threat alerts for your apps.")
def monitor_alerts(payload: ThreatQueryRequest, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    events = get_threat_events(db, auth.user_id, payload.app_id, payload.unresolved_only)
    return [{"id": e.id, "app_id": e.app_id, "threat_type": e.threat_type,
             "severity": e.severity, "detail": e.detail,
             "resolved": e.resolved, "created_at": e.created_at.isoformat()} for e in events]


@app.post("/quantum/monitor/resolve/{threat_id}", tags=["Monitoring"], summary="Mark a threat event as resolved.")
def monitor_resolve(threat_id: str, auth: models.APIKey = Depends(authenticate), db: Session = Depends(get_db)):
    try:
        return resolve_threat(db, threat_id, auth.user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
