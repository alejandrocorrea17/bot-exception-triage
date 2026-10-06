CREATE TABLE IF NOT EXISTS bot_exceptions (
    id             BIGSERIAL PRIMARY KEY,
    robot_name     TEXT NOT NULL,
    process_name   TEXT NOT NULL,
    exception_type TEXT,
    message        TEXT NOT NULL,
    -- Segunda línea de defensa: la base rechaza valores inválidos aunque alguien salte la API
    severity       TEXT NOT NULL DEFAULT 'medium' CHECK (severity IN ('low', 'medium', 'high')),
    occurred_at    TIMESTAMPTZ NOT NULL,
    received_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);