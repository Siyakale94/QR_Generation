from __future__ import annotations

import os
from functools import lru_cache
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from supabase import Client, create_client

load_dotenv()


# ── Singleton Supabase client ─────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _get_client() -> Client:
    url: str = os.environ.get("SUPABASE_URL", "").strip()
    key: str = os.environ.get("SUPABASE_SERVICE_KEY", "").strip()

    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in your .env file."
        )
    return create_client(url, key)


# ── Service class ─────────────────────────────────────────────────────────────

class SupabaseService:
    """Thin wrapper around the Supabase PostgREST client."""

    def __init__(self) -> None:
        self._client: Client = _get_client()

    # ── user_profiles ────────────────────────────────────────────────────────

    def insert_athlete(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new athlete row and return the created record."""
        response = (
            self._client
            .table("user_profiles")
            .insert(payload)
            .execute()
        )
        if not response.data:
            raise RuntimeError(f"Supabase insert failed: {response}")
        return response.data[0]

    def get_athlete_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Fetch an athlete by their QR token. Returns None if not found."""
        response = (
            self._client
            .table("user_profiles")
            .select("*")
            .eq("qr_token", token)
            .maybe_single()
            .execute()
        )
        return response.data  # None when no match

    def get_athlete_by_id(self, athlete_id: str) -> Optional[Dict[str, Any]]:
        """Fetch an athlete by their UUID. Returns None if not found."""
        response = (
            self._client
            .table("user_profiles")
            .select("*")
            .eq("user_id", athlete_id)
            .maybe_single()
            .execute()
        )
        return response.data

    # ── scan_events ──────────────────────────────────────────────────────────

    def insert_scan_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Record a QR scan event and return the created record."""
        response = (
            self._client
            .table("scan_events")
            .insert(payload)
            .execute()
        )
        if not response.data:
            raise RuntimeError(f"Supabase scan_events insert failed: {response}")
        return response.data[0]

    def get_scan_events_for_athlete(self, athlete_id: str) -> list[Dict[str, Any]]:
        """Return all scan events for a given athlete, newest first."""
        response = (
            self._client
            .table("scan_events")
            .select("*")
            .eq("athlete_id", athlete_id)
            .order("scanned_at", desc=True)
            .execute()
        )
        return response.data or []
