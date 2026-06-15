"""
Cryptographically random token generation for QR codes.

Each token is a standard UUID4 (128 bits of randomness produced by the OS
CSPRNG via ``os.urandom``).  Only the token is embedded in the QR image –
never the athlete's PII – so a lost/replayed token cannot be used to fake
identity without a valid DB record.
"""

import uuid


def generate_qr_token() -> str:
    """Return a new cryptographically random UUID4 string (lowercase, hyphenated)."""
    return str(uuid.uuid4())
