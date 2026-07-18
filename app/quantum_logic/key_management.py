# Original Author: Oluwatosin Olalere (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

from datetime import datetime, timedelta
from collections import defaultdict
from sqlalchemy.orm import Session
from app import models
from app.quantum_logic.cryptography import generate_quantum_key

# In-memory store for replay and brute-force detection
_auth_fail_store: dict[str, list[datetime]] = defaultdict(list)
_used_tokens: set[str] = set()

BRUTE_FORCE_THRESHOLD = 5   # failed auths within window
BRUTE_FORCE_WINDOW = 60     # seconds


def issue_key(db: Session, user_id: str, app_id: str, key_bits: int = 256,
              ttl_hours: int | None = None) -> models.ManagedKey:
    expires_at = datetime.utcnow() + timedelta(hours=ttl_hours) if ttl_hours else None
    record = models.ManagedKey(
        user_id=user_id,
        app_id=app_id,
        key_value=generate_quantum_key(key_bits),
        key_bits=str(key_bits),
        status="active",
        expires_at=expires_at,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    _write_audit(db, user_id, app_id, "key_issued", f"key_id={record.id} bits={key_bits}")
    return record


def rotate_key(db: Session, key_id: str, user_id: str) -> models.ManagedKey:
    record = db.query(models.ManagedKey).filter(
        models.ManagedKey.id == key_id,
        models.ManagedKey.user_id == user_id,
    ).first()
    if not record:
        raise ValueError("Key not found.")
    if record.status == "revoked":
        raise ValueError("Cannot rotate a revoked key.")

    record.previous_key = record.key_value
    record.key_value = generate_quantum_key(int(record.key_bits))
    record.status = "active"
    db.commit()
    db.refresh(record)
    _write_audit(db, user_id, record.app_id, "key_rotated", f"key_id={key_id}")
    return record


def revoke_key(db: Session, key_id: str, user_id: str) -> dict:
    record = db.query(models.ManagedKey).filter(
        models.ManagedKey.id == key_id,
        models.ManagedKey.user_id == user_id,
    ).first()
    if not record:
        raise ValueError("Key not found.")
    record.status = "revoked"
    db.commit()
    _write_audit(db, user_id, record.app_id, "key_revoked", f"key_id={key_id}")
    return {"key_id": key_id, "status": "revoked"}


def verify_managed_key(db: Session, key_id: str, key_value: str,
                       ip_address: str | None = None) -> dict:
    """Verify a managed key and detect threats (replay, brute force, revoked use)."""
    record = db.query(models.ManagedKey).filter(models.ManagedKey.id == key_id).first()

    if not record:
        return {"valid": False, "reason": "key_not_found"}

    # Replay detection: same key_value used more than once
    token_fingerprint = f"{key_id}:{key_value}"
    if token_fingerprint in _used_tokens:
        _record_threat(db, record.user_id, record.app_id, "replay",
                       "high", f"Replay attempt on key_id={key_id}", ip_address)
        return {"valid": False, "reason": "replay_detected"}

    # Revoked key use
    if record.status == "revoked":
        _record_threat(db, record.user_id, record.app_id, "revoked_key_use",
                       "high", f"Attempt to use revoked key_id={key_id}", ip_address)
        return {"valid": False, "reason": "key_revoked"}

    # Expiry check
    if record.expires_at and datetime.utcnow() > record.expires_at:
        return {"valid": False, "reason": "key_expired"}

    # Value mismatch → brute force tracking
    if record.key_value != key_value:
        _track_auth_failure(db, record.user_id, record.app_id, key_id, ip_address)
        return {"valid": False, "reason": "invalid_key"}

    _used_tokens.add(token_fingerprint)
    _write_audit(db, record.user_id, record.app_id, "auth_ok",
                 f"key_id={key_id}", ip_address)
    return {"valid": True, "app_id": record.app_id, "key_id": key_id}


def get_audit_logs(db: Session, user_id: str, app_id: str | None = None,
                   limit: int = 50) -> list:
    q = db.query(models.AuditLog).filter(models.AuditLog.user_id == user_id)
    if app_id:
        q = q.filter(models.AuditLog.app_id == app_id)
    return q.order_by(models.AuditLog.created_at.desc()).limit(limit).all()


def get_threat_events(db: Session, user_id: str, app_id: str | None = None,
                      unresolved_only: bool = True) -> list:
    q = db.query(models.ThreatEvent).filter(models.ThreatEvent.user_id == user_id)
    if app_id:
        q = q.filter(models.ThreatEvent.app_id == app_id)
    if unresolved_only:
        q = q.filter(models.ThreatEvent.resolved == False)
    return q.order_by(models.ThreatEvent.created_at.desc()).all()


def resolve_threat(db: Session, threat_id: str, user_id: str) -> dict:
    event = db.query(models.ThreatEvent).filter(
        models.ThreatEvent.id == threat_id,
        models.ThreatEvent.user_id == user_id,
    ).first()
    if not event:
        raise ValueError("Threat event not found.")
    event.resolved = True
    db.commit()
    return {"threat_id": threat_id, "resolved": True}


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _write_audit(db: Session, user_id: str, app_id: str, event_type: str,
                 detail: str, ip_address: str | None = None):
    db.add(models.AuditLog(
        user_id=user_id, app_id=app_id,
        event_type=event_type, detail=detail, ip_address=ip_address,
    ))
    db.commit()


def _record_threat(db: Session, user_id: str, app_id: str, threat_type: str,
                   severity: str, detail: str, ip_address: str | None = None):
    db.add(models.ThreatEvent(
        user_id=user_id, app_id=app_id,
        threat_type=threat_type, severity=severity, detail=detail,
    ))
    _write_audit(db, user_id, app_id, f"threat_{threat_type}", detail, ip_address)
    db.commit()


def _track_auth_failure(db: Session, user_id: str, app_id: str,
                        key_id: str, ip_address: str | None):
    now = datetime.utcnow()
    store_key = f"{user_id}:{app_id}"
    _auth_fail_store[store_key] = [
        t for t in _auth_fail_store[store_key]
        if (now - t).seconds < BRUTE_FORCE_WINDOW
    ]
    _auth_fail_store[store_key].append(now)
    _write_audit(db, user_id, app_id, "auth_fail", f"key_id={key_id}", ip_address)

    if len(_auth_fail_store[store_key]) >= BRUTE_FORCE_THRESHOLD:
        _record_threat(db, user_id, app_id, "brute_force", "critical",
                       f"{BRUTE_FORCE_THRESHOLD} failed auth attempts in {BRUTE_FORCE_WINDOW}s from {ip_address}",
                       ip_address)
