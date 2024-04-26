import math

EFFECTIVE_REACH_A = 4.08577
EFFECTIVE_REACH_B = 3.08577


def effective_reach(x, R):
    return (2.0 / EFFECTIVE_REACH_A) * (math.atan(((EFFECTIVE_REACH_A * x) / R) - EFFECTIVE_REACH_B) -
                                        math.atan(-EFFECTIVE_REACH_B))


def avg_effective_reach(a, b, R):
    return (effective_reach(a, R) + effective_reach(b, R)) / 2.0


