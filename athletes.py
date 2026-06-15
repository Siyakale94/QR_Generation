from fastapi import APIRouter, HTTPException, status
from athlete import (
    AthleteCreate,
    AthleteCreateResponse,
    AthleteProfile
)

from supabase_service import SupabaseService
from qr_service import QRService
from token_utils import generate_qr_token


router = APIRouter(prefix="/athletes", tags=["Athletes"])

_supabase = SupabaseService()
_qr = QRService()


# ── POST /athletes ────────────────────────────────────────────────────────────

@router.post(
    "",
    response_model=AthleteCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new athlete and generate their QR code",
)
def create_athlete(body: AthleteCreate) -> AthleteCreateResponse:
    """
    Validate the incoming payload, assign a cryptographic QR token,
    persist to Supabase, generate a QR PNG and return the full record.
    """
    # 1 – Generate token
    token = generate_qr_token()

    # 2 – Build DB payload
    payload: dict = {
        "user_name": body.user_name,
        "dob": str(body.dob),           # ISO-8601 date string
        "gender": body.gender,
        "sport": body.sport,
        "team_club": body.team_club,
        "height": body.height,
        "weight": body.weight,
        "qr_token": token,
    }

    # 3 – Insert into Supabase
    try:
        record = _supabase.insert_athlete(payload)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Database error: {exc}",
        )

    athlete_id: str = record["user_id"]

    # 4 – Generate QR PNG (token only stored in image)
    try:
        qr_path = _qr.generate(athlete_id=athlete_id, token=token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"QR generation error: {exc}",
        )

    # 5 – Build and return response
    profile = AthleteProfile(**record)

    return AthleteCreateResponse(
        athlete_id=athlete_id,
        qr_token=token,
        qr_png_path=qr_path,
        profile=profile,
    )


# ── GET /athletes/token/{token} ───────────────────────────────────────────────

@router.get(
    "/token/{token}",
    response_model=AthleteProfile,
    summary="Look up an athlete by their QR token",
)
def get_athlete_by_token(token: str) -> AthleteProfile:
    """Resolve a scanned QR token to the athlete's full profile."""
    try:
        record = _supabase.get_athlete_by_token(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Database error: {exc}",
        )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No athlete found for the provided token.",
        )

    return AthleteProfile(**record)
