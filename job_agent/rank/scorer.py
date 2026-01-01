# rank/scorer.py



def combine_scores(
    semantic: float,
    lexical: float,
    signals: dict,
    penalty: float = 0.0,
) -> dict:
    final = (
        0.55 * semantic +
        0.30 * lexical +
        0.10 * signals.get("skill_overlap", 0.0) +
        0.03 * signals.get("ml_depth", 0.0) +
        0.02 * signals.get("ownership", 0.0) -
        penalty
    )

    return {
        "final": final,
        "semantic": semantic,
        "lexical": lexical,
        **signals,
        "penalty": penalty,
    }
