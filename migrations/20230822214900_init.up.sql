CREATE TABLE IF NOT EXISTS users (
    id SERIAL NOT NULL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT,
    "level" INT,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS onboarding_questions (
    id SERIAL NOT NULL PRIMARY KEY,
    "order" INT NOT NULL,
    text TEXT NOT NULL,
    answer TEXT NOT NULL,
    choices JSON NOT NULL,
    "level" INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users_onboarding_questions (
    answer TEXT NOT NULL,
    onboarding_question_id INT NOT NULL REFERENCES onboarding_questions (id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_onboarding_questions_user_id_question_id_idx ON users_onboarding_questions(user_id, onboarding_question_id);

CREATE TABLE IF NOT EXISTS questions (
    id SERIAL NOT NULL PRIMARY KEY,
    text TEXT NOT NULL,
    answer TEXT NOT NULL,
    choices JSON NOT NULL,
    "level" INT NOT NULL,
    explanation TEXT,
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
