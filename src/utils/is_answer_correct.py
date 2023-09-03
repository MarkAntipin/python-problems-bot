def _preprocess_answers(answer: str) -> str:
    return answer.strip().lower()


def is_answer_correct(user_answer: str, correct_answer: str) -> bool:
    return _preprocess_answers(user_answer) == _preprocess_answers(correct_answer)
