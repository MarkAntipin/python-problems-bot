CREATE TABLE IF NOT EXISTS advices (
    id SERIAL NOT NULL PRIMARY KEY,
    theme TEXT NOT NULL,
    level INT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_advices (
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    advice_id INT NOT NULL REFERENCES questions (id) ON DELETE CASCADE,
    user_feedback INT NOT NULL DEFAULT 0,
    is_useful BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_advices_user_id_advice_id_idx ON users_advices(user_id, advice_id);
CREATE INDEX IF NOT EXISTS users_advices_user_id_created_at_idx ON users_advices(user_id, created_at);


CREATE TABLE IF NOT EXISTS users_send_advices (
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    advice_id INT NOT NULL REFERENCES advices (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_send_advices_user_id_advice_id_idx ON users_send_advices(user_id, advice_id);