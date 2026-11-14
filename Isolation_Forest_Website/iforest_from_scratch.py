"""
A small, readable Isolation Forest written directly from the pseudocode in
Liu, Ting and Zhou (2008): Algorithm 1 (iForest), Algorithm 2 (iTree) and
Algorithm 3 (PathLength).

It is only used for learning and for checking the pseudocode. The website demo
uses sklearn.ensemble.IsolationForest.
"""
import math
import random

EULER = 0.5772156649


def c(n):
    """Average path length of an unsuccessful search in a BST with n items (Equation 1)."""
    if n <= 1:
        return 0.0
    if n == 2:
        return 1.0
    harmonic = math.log(n - 1) + EULER
    return 2.0 * harmonic - 2.0 * (n - 1) / n


class ExNode:
    def __init__(self, size):
        self.size = size


class InNode:
    def __init__(self, left, right, split_att, split_value):
        self.left = left
        self.right = right
        self.split_att = split_att
        self.split_value = split_value


def itree(X, e, l, rng):
    """Algorithm 2. X is a list of points (lists of numbers), e is the current height, l the limit."""
    if e >= l or len(X) <= 1:
        return ExNode(len(X))
    q = rng.randrange(len(X[0]))                    # random attribute
    lo = min(x[q] for x in X)
    hi = max(x[q] for x in X)
    if lo == hi:                                    # all values equal: cannot split on q
        # The paper stops when all data in X are the same. Here we try other attributes first.
        usable = [a for a in range(len(X[0])) if min(x[a] for x in X) != max(x[a] for x in X)]
        if not usable:
            return ExNode(len(X))
        q = rng.choice(usable)
        lo = min(x[q] for x in X)
        hi = max(x[q] for x in X)
    p = rng.uniform(lo, hi)                         # random split value
    Xl = [x for x in X if x[q] < p]
    Xr = [x for x in X if x[q] >= p]
    return InNode(itree(Xl, e + 1, l, rng), itree(Xr, e + 1, l, rng), q, p)


def iforest(X, t=100, psi=256, seed=42):
    """Algorithm 1."""
    rng = random.Random(seed)
    psi = min(psi, len(X))
    l = math.ceil(math.log2(max(psi, 2)))           # height limit
    forest = []
    for _ in range(t):
        sample = rng.sample(X, psi)                 # without replacement
        forest.append(itree(sample, 0, l, rng))
    return forest, psi


def path_length(x, T, e=0):
    """Algorithm 3."""
    if isinstance(T, ExNode):
        return e + c(T.size)
    if x[T.split_att] < T.split_value:
        return path_length(x, T.left, e + 1)
    return path_length(x, T.right, e + 1)


def anomaly_score(x, forest, psi):
    """Equation 2: s(x, psi) = 2 ** (-E[h(x)] / c(psi))."""
    mean_h = sum(path_length(x, T) for T in forest) / len(forest)
    return 2.0 ** (-mean_h / c(psi))
