-- ============================================================
-- Athlete QR Identification System - Supabase Schema
-- Run this in your Supabase SQL editor to set up the database
-- ============================================================

-- Enable the pgcrypto extension for gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================
-- Table: user_profiles
-- ============================================================
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id      UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    user_name    TEXT        NOT NULL,
    dob          DATE        NOT NULL,
    gender       TEXT        NOT NULL,
    sport        TEXT        NOT NULL,
    team_club    TEXT,
    height       NUMERIC(5, 2),
    weight       NUMERIC(5, 2),
    qr_token     TEXT        UNIQUE NOT NULL,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Index on qr_token for fast token lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_qr_token
    ON user_profiles (qr_token);

-- ============================================================
-- Table: scan_events
-- ============================================================
CREATE TABLE IF NOT EXISTS scan_events (
    id           UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    athlete_id   UUID        NOT NULL REFERENCES user_profiles(user_id) ON DELETE CASCADE,
    scanned_at   TIMESTAMPTZ DEFAULT NOW(),
    location     TEXT,
    event_name   TEXT
);

-- Index on athlete_id for fast scan history lookups
CREATE INDEX IF NOT EXISTS idx_scan_events_athlete_id
    ON scan_events (athlete_id);

-- ============================================================
-- Row Level Security (optional – enable if using anon key)
-- ============================================================
-- ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE scan_events   ENABLE ROW LEVEL SECURITY;

-- Allow service-role full access (already default); uncomment
-- policies below only if you restrict with anon/authenticated keys.

-- CREATE POLICY "service role full access" ON user_profiles
--     USING (true) WITH CHECK (true);

-- CREATE POLICY "service role full access" ON scan_events
--     USING (true) WITH CHECK (true);
