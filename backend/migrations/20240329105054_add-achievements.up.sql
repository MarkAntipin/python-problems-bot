CREATE TABLE IF NOT EXISTS users_achievements (
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    achievement_name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_achievements_user_id_idx ON users_achievements(user_id);
