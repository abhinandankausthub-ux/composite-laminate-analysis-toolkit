import numpy as np


def compute_nu21(E1, E2, nu12):
    """
    Compute minor Poisson ratio using reciprocity relation
    """
    return nu12 * (E2 / E1)


def reduced_stiffness_matrix(material):
    """
    Compute reduced stiffness matrix Q for a lamina

    Parameters
    ----------
    material : dict
        Dictionary containing material properties
        E1, E2, G12, nu12

    Returns
    -------
    Q : numpy array (3x3)
        Reduced stiffness matrix
    """

    E1 = material["E1"]
    E2 = material["E2"]
    G12 = material["G12"]
    nu12 = material["nu12"]

    nu21 = compute_nu21(E1, E2, nu12)

    denom = 1 - nu12 * nu21

    Q11 = E1 / denom
    Q22 = E2 / denom
    Q12 = (nu12 * E2) / denom
    Q66 = G12

    Q = np.array([
        [Q11, Q12, 0],
        [Q12, Q22, 0],
        [0,   0,   Q66]
    ])

    return Q
