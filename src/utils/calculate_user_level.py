def calculate_user_level(correct_answer_levels: list[int], all_answers_levels: list[int]) -> int:
    total_possible_score = sum(all_answers_levels)
    total_user_score = sum(correct_answer_levels)

    relative_performance = total_user_score / total_possible_score

    if relative_performance >= 0.8:
        return 3
    elif relative_performance >= 0.6:
        return 2
    else:
        return 1
