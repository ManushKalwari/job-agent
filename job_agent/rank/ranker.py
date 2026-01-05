import math

def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))

def poe_score(
    sem: float,
    lex: float,
    mu_s: float,
    sd_s: float,
    mu_l: float,
    sd_l: float,
    eps: float = 1e-6,
    a: float = 1.0,
    b: float = 1.0,
) -> float:
    # z-score then sigmoid -> (0,1)
    ps = _sigmoid((sem - mu_s) / (sd_s + 1e-9))
    pl = _sigmoid((lex - mu_l) / (sd_l + 1e-9))
    return a * math.log(ps + eps) + b * math.log(pl + eps)