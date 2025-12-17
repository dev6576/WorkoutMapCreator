def score_candidate(length_diff, shape_score, anchor_bonus):
    return (
        -length_diff * 0.4
        -shape_score * 0.5
        +anchor_bonus
    )
