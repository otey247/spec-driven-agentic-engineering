PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS requests (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL CHECK (length(title) BETWEEN 3 AND 120),
    description TEXT NOT NULL CHECK (length(description) BETWEEN 5 AND 4000),
    created_by TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
      CHECK (status IN ('pending', 'approved', 'rejected')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    version INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_requests_creator ON requests(created_by, created_at);
CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status, created_at);
CREATE TABLE IF NOT EXISTS audit_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id TEXT NOT NULL REFERENCES requests(id),
    actor_id TEXT NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('created', 'approved', 'rejected')),
    note TEXT NOT NULL DEFAULT '',
    at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_request ON audit_events(request_id, id);
