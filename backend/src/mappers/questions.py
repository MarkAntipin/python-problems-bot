import json

import asyncpg

from src.models.questions import Question


def map_question_from_pg_row(row: asyncpg.Record) -> Question:
    row_dict = dict(row)
    row_dict['choices'] = json.loads(row_dict['choices'])
    return Question.model_validate(row_dict)
