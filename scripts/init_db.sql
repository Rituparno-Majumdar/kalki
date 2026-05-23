-- Kalki PostgreSQL schema
-- Run automatically by Docker on first container start.
-- Re-run manually: psql $DATABASE_URL -f scripts/init_db.sql

-- ---------------------------------------------------------------------------
-- kalki_records — raw connector output (one row per KalkiRecord)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kalki_records (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Provenance
    source_name         TEXT        NOT NULL,
    source_url          TEXT        NOT NULL,
    connector_version   TEXT        NOT NULL,
    raw_source_hash     TEXT,

    -- Classification
    module              TEXT        NOT NULL,  -- e.g. 'kalki_prakriti'

    -- Location (India admin hierarchy)
    state               TEXT        NOT NULL,
    district            TEXT        NOT NULL,
    block               TEXT,
    village             TEXT,
    state_code          TEXT,       -- ISO 3166-2, e.g. 'IN-OD'
    district_lgd_code   TEXT,       -- LGD district code

    -- Spatiotemporal
    record_timestamp    TIMESTAMPTZ NOT NULL,
    fetch_timestamp     TIMESTAMPTZ NOT NULL DEFAULT now(),

    -- Payload
    data                JSONB       NOT NULL DEFAULT '{}',

    -- Quality
    data_quality_score  REAL        NOT NULL DEFAULT 0.0
        CHECK (data_quality_score >= 0.0 AND data_quality_score <= 1.0),

    -- Audit
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_records_module       ON kalki_records (module);
CREATE INDEX IF NOT EXISTS idx_records_district     ON kalki_records (state, district);
CREATE INDEX IF NOT EXISTS idx_records_timestamp    ON kalki_records (record_timestamp);
CREATE INDEX IF NOT EXISTS idx_records_lgd          ON kalki_records (district_lgd_code);
CREATE INDEX IF NOT EXISTS idx_records_data         ON kalki_records USING GIN (data);

-- ---------------------------------------------------------------------------
-- kalki_signals — processed analytical signals (one row per KalkiSignal)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kalki_signals (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Classification
    module              TEXT        NOT NULL,
    signal_type         TEXT        NOT NULL,  -- risk_score / anomaly / forecast / etc.
    severity            TEXT        NOT NULL,  -- info / low / medium / high / critical

    -- Location
    state               TEXT        NOT NULL,
    district            TEXT        NOT NULL,
    block               TEXT,
    state_code          TEXT,
    district_lgd_code   TEXT,

    -- Time scope of the signal
    period_start        TIMESTAMPTZ NOT NULL,
    period_end          TIMESTAMPTZ NOT NULL,

    -- Signal value (flexible JSONB to accommodate all signal_type variants)
    value               JSONB       NOT NULL,
    confidence          REAL        NOT NULL
        CHECK (confidence >= 0.0 AND confidence <= 1.0),

    -- Human-readable label
    label               TEXT        NOT NULL DEFAULT '',

    -- Ethics
    demographic_flag    BOOLEAN     NOT NULL DEFAULT FALSE,
    population_count    INTEGER,

    -- Model metadata
    model_name          TEXT,
    model_version       TEXT,

    -- Source records
    source_record_ids   UUID[]      DEFAULT '{}',

    -- Audit
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_signals_module       ON kalki_signals (module);
CREATE INDEX IF NOT EXISTS idx_signals_district     ON kalki_signals (state, district);
CREATE INDEX IF NOT EXISTS idx_signals_type         ON kalki_signals (signal_type);
CREATE INDEX IF NOT EXISTS idx_signals_severity     ON kalki_signals (severity);
CREATE INDEX IF NOT EXISTS idx_signals_period       ON kalki_signals (period_start, period_end);
CREATE INDEX IF NOT EXISTS idx_signals_demo_flag    ON kalki_signals (demographic_flag) WHERE demographic_flag = TRUE;

-- ---------------------------------------------------------------------------
-- kalki_briefings — Intelligence Layer outputs (human review queue)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS kalki_briefings (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    module              TEXT        NOT NULL,
    audience            TEXT        NOT NULL,  -- journalist / district_collector / researcher / public

    -- Location
    state               TEXT        NOT NULL,
    district            TEXT        NOT NULL,
    state_code          TEXT,
    district_lgd_code   TEXT,

    -- Time scope
    period_start        TIMESTAMPTZ NOT NULL,
    period_end          TIMESTAMPTZ NOT NULL,

    -- Content
    situation_summary   TEXT        NOT NULL,
    evidence            JSONB       NOT NULL DEFAULT '[]',
    recommended_actions JSONB       NOT NULL DEFAULT '[]',
    data_limitations    JSONB       NOT NULL DEFAULT '[]',
    overall_confidence  REAL        NOT NULL DEFAULT 0.0,

    -- Source signals
    source_signal_ids   UUID[]      DEFAULT '{}',

    -- Human review workflow (required by ETHICS.md)
    review_status       TEXT        NOT NULL DEFAULT 'pending'
        CHECK (review_status IN ('pending', 'approved', 'rejected', 'escalated')),
    reviewer            TEXT,
    reviewer_notes      TEXT,

    -- Audit
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
    published_at        TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_briefings_review     ON kalki_briefings (review_status);
CREATE INDEX IF NOT EXISTS idx_briefings_module     ON kalki_briefings (module);
CREATE INDEX IF NOT EXISTS idx_briefings_district   ON kalki_briefings (state, district);
