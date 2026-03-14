import numpy as np

from modules.stiffness_matrix import reduced_stiffness_matrix
from modules.transformation import transform_Q


def compute_ABD(material, stacking_sequence, ply_thickness):
    """
    Compute ABD matrix for a laminate

    Parameters
    ----------
    material : dict
        Material properties
    stacking_sequence : list
        Ply angles [0,45,-45,90]
    ply_thickness : float
        Thickness of each ply

    Returns
    -------
    A, B, D : numpy arrays (3x3)
    """

    n = len(stacking_sequence)

    Q = reduced_stiffness_matrix(material)

    total_thickness = n * ply_thickness

    z = np.linspace(-total_thickness/2, total_thickness/2, n+1)

    A = np.zeros((3,3))
    B = np.zeros((3,3))
    D = np.zeros((3,3))

    for k in range(n):

        theta = stacking_sequence[k]

        Q_bar = transform_Q(Q, theta)

        z_k = z[k+1]
        z_k1 = z[k]

        A += Q_bar * (z_k - z_k1)

        B += 0.5 * Q_bar * (z_k**2 - z_k1**2)

        D += (1/3) * Q_bar * (z_k**3 - z_k1**3)

    return A, B, D
