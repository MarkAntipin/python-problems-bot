ALTER TABLE users ADD COLUMN level INT NOT NULL DEFAULT 2;

ALTER TABLE questions
ADD COLUMN level INT NOT NULL DEFAULT 2,
ADD COLUMN external_id INT,
ADD COLUMN theme TEXT;
