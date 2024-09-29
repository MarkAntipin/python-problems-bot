CREATE TABLE IF NOT EXISTS coding_questions (
    id SERIAL NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    problem TEXT NOT NULL,
    params TEXT NOT NULL,
    return_type TEXT NOT NULL,
    difficulty TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS users_coding_questions (
    coding_question_id INT NOT NULL REFERENCES coding_questions (id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS users_coding_questions_user_id_coding_question_id_idx ON users_coding_questions(user_id, coding_question_id);
CREATE INDEX IF NOT EXISTS users_coding_questions_user_id_coding_created_at_idx ON users_coding_questions(user_id, created_at);

CREATE TABLE IF NOT EXISTS coding_questions_tests (
    coding_question_id INT NOT NULL REFERENCES coding_questions (id) ON DELETE CASCADE,
    input TEXT NOT NULL,
    output TEXT NOT NULL
);
