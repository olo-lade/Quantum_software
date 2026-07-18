# Original Author: Oluwatosin Olalere (GitHub: olo-lade)
# Repository: https://github.com/olo-lade/Quantum_software
# License: CC BY 4.0 — Credit required for any use or derivative work.

import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# 32-byte key required for AES-256. Must be set in .env as a 64-char hex string.
_raw = os.getenv("DB_ENCRYPTION_KEY", "")


def _get_key() -> bytes:
    if not _raw or len(_raw) != 64:
        raise RuntimeError(
            "DB_ENCRYPTION_KEY must be a 64-character hex string in .env. "
            "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    return bytes.fromhex(_raw)


def encrypt_value(plaintext: str) -> str:
    """Encrypt a string with AES-256-GCM. Returns base64(nonce + ciphertext)."""
    aesgcm = AESGCM(_get_key())
    nonce = os.urandom(12)                          # 96-bit nonce, unique per encryption
    ct = aesgcm.encrypt(nonce, plaintext.encode(), None)
    return base64.b64encode(nonce + ct).decode()


def decrypt_value(token: str) -> str:
    """Decrypt a value produced by encrypt_value."""
    raw = base64.b64decode(token)
    nonce, ct = raw[:12], raw[12:]
    aesgcm = AESGCM(_get_key())
    return aesgcm.decrypt(nonce, ct, None).decode()
