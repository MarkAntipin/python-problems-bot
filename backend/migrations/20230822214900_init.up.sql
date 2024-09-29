CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT,
    came_from TEXT,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL NOT NULL PRIMARY KEY,
    text TEXT NOT NULL,
    answer TEXT NOT NULL,
    choices JSON NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_questions (
    answer TEXT NOT NULL,
    question_id INT NOT NULL REFERENCES questions (id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_questions_user_id_question_id_idx ON users_questions(user_id, question_id);
CREATE INDEX IF NOT EXISTS users_questions_user_id_created_at_idx ON users_questions(user_id, created_at);


CREATE TABLE IF NOT EXISTS users_send_questions (
    question_id INT NOT NULL REFERENCES questions (id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_send_questions_user_id_question_id_idx ON users_send_questions(user_id, question_id);
