from __future__ import annotations

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from qr_service import QRService
from supabase_service import SupabaseService

router = APIRouter(prefix="/athletes", tags=["QR Codes"])

_supabase = SupabaseService()
_qr = QRService()


# ── GET /athletes/{athlete_id}/qr ─────────────────────────────────────────────

@router.get(
    "/{athlete_id}/qr",
    response_class=FileResponse,
    summary="Download the QR PNG for an athlete",
    responses={
        200: {"content": {"image/png": {}}, "description": "QR code PNG image"},
        404: {"description": "Athlete not found or QR not yet generated"},
    },
)
def get_athlete_qr(athlete_id: str) -> FileResponse:
    """
    Return the pre-generated QR code PNG for the given athlete UUID.

    The file is served directly from the ``generated_qr/`` directory.
    A 404 is returned if the athlete does not exist in the database or
    if the PNG file has not been generated yet.
    """
    # Confirm the athlete exists
    try:
        record = _supabase.get_athlete_by_id(athlete_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Database error: {exc}",
        )

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No athlete found with ID '{athlete_id}'.",
        )

    # Resolve file path
    qr_path = _qr.get_path(athlete_id)

    if not qr_path.exists():
        # Athlete exists but QR PNG is missing – regenerate on the fly
        try:
            _qr.generate(athlete_id=athlete_id, token=record["qr_token"])
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"QR regeneration failed: {exc}",
            )

    return FileResponse(
        path=str(qr_path),
        media_type="image/png",
        filename=f"{athlete_id}.png",
    )
