from __future__ import annotations

import os
from pathlib import Path

import qrcode
from qrcode.image.pil import PilImage
from dotenv import load_dotenv

load_dotenv()

# Directory where QR PNG files are stored (configurable via .env)
_QR_DIR = Path(os.environ.get("QR_OUTPUT_DIR", "generated_qr"))


class QRService:
    """Generates QR-code PNG files from opaque tokens."""

    def __init__(self) -> None:
        _QR_DIR.mkdir(parents=True, exist_ok=True)

    def generate(self, athlete_id: str, token: str) -> str:
        """
        Create a QR code PNG that encodes *only* the token.

        Parameters
        ----------
        athlete_id : str
            Used as the filename (``generated_qr/<athlete_id>.png``).
        token : str
            The opaque UUID token stored in the QR image.

        Returns
        -------
        str
            Relative path to the saved PNG, e.g. ``generated_qr/abc-123.png``.
        """
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(token)
        qr.make(fit=True)

        img: PilImage = qr.make_image(fill_color="black", back_color="white")

        file_path: Path = _QR_DIR / f"{athlete_id}.png"
        img.save(str(file_path))

        return str(file_path)

    def get_path(self, athlete_id: str) -> Path:
        """Return the expected Path for an athlete's QR PNG."""
        return _QR_DIR / f"{athlete_id}.png"
