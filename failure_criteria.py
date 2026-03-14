import numpy as np


# -------------------------------------------------
# Maximum Stress Criterion
# -------------------------------------------------

def maximum_stress_failure(stress, material):

    """
    Maximum stress failure criterion
    """

    s1, s2, t12 = stress

    Xt = material["Xt"]
    Xc = material["Xc"]
    Yt = material["Yt"]
    Yc = material["Yc"]
    S = material["S"]

    # Fiber direction
    if s1 >= 0:
        f1 = s1 / Xt
    else:
        f1 = abs(s1) / Xc

    # Transverse direction
    if s2 >= 0:
        f2 = s2 / Yt
    else:
        f2 = abs(s2) / Yc

    # Shear
    f6 = abs(t12) / S

    return max(f1, f2, f6)


# -------------------------------------------------
# Tsai-Hill Criterion
# -------------------------------------------------

def tsai_hill_failure(stress, material):

    """
    Tsai-Hill failure criterion
    """

    s1, s2, t12 = stress

    Xt = material["Xt"]
    Xc = material["Xc"]
    Yt = material["Yt"]
    Yc = material["Yc"]
    S = material["S"]

    # Select appropriate strengths
    X = Xt if s1 >= 0 else Xc
    Y = Yt if s2 >= 0 else Yc

    FI = (
        (s1 / X) ** 2
        + (s2 / Y) ** 2
        - (s1 * s2) / (X * Y)
        + (t12 / S) ** 2
    )

    return FI


# -------------------------------------------------
# Tsai-Wu Criterion
# -------------------------------------------------

def tsai_wu_failure(stress, material):

    """
    Tsai-Wu failure criterion
    """

    s1, s2, t12 = stress

    Xt = material["Xt"]
    Xc = material["Xc"]
    Yt = material["Yt"]
    Yc = material["Yc"]
    S = material["S"]

    # Tsai-Wu coefficients
    F1 = (1 / Xt) - (1 / Xc)
    F11 = 1 / (Xt * Xc)

    F2 = (1 / Yt) - (1 / Yc)
    F22 = 1 / (Yt * Yc)

    F66 = 1 / (S ** 2)

    F12 = -0.5 * np.sqrt(F11 * F22)

    FI = (
        F1 * s1
        + F2 * s2
        + F11 * s1**2
        + F22 * s2**2
        + F66 * t12**2
        + 2 * F12 * s1 * s2
    )

    return FI
