from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


# ── Request body for POST /athletes ──────────────────────────────────────────

class AthleteCreate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=120, description="Full name of the athlete")
    dob: date = Field(..., description="Date of birth (YYYY-MM-DD)")
    gender: str = Field(..., description="Gender identity")
    sport: str = Field(..., min_length=1, max_length=80, description="Primary sport")
    team_club: Optional[str] = Field(None, max_length=120, description="Team or club name")
    height: Optional[float] = Field(None, gt=0, lt=300, description="Height in centimetres")
    weight: Optional[float] = Field(None, gt=0, lt=500, description="Weight in kilograms")

    @field_validator("dob")
    @classmethod
    def dob_not_future(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        return v

    @field_validator("gender")
    @classmethod
    def gender_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("gender must not be blank.")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_name": "Arjun Sharma",
                "dob": "2000-05-15",
                "gender": "Male",
                "sport": "Athletics",
                "team_club": "Mumbai Runners",
                "height": 175.0,
                "weight": 68.5,
            }
        }
    }


# ── Full profile returned from DB ─────────────────────────────────────────────

class AthleteProfile(BaseModel):
    user_id: UUID
    user_name: str
    dob: date
    gender: str
    sport: str
    team_club: Optional[str]
    height: Optional[float]
    weight: Optional[float]
    qr_token: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Response body for POST /athletes ─────────────────────────────────────────

class AthleteCreateResponse(BaseModel):
    athlete_id: UUID
    qr_token: str
    qr_png_path: str
    profile: AthleteProfile


# ── Scan event models ─────────────────────────────────────────────────────────

class ScanEventCreate(BaseModel):
    athlete_id: UUID
    location: Optional[str] = None
    event_name: Optional[str] = None


class ScanEvent(BaseModel):
    id: UUID
    athlete_id: UUID
    scanned_at: datetime
    location: Optional[str]
    event_name: Optional[str]

    model_config = {"from_attributes": True}
