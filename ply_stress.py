import numpy as np

from modules.stiffness_matrix import reduced_stiffness_matrix
from modules.transformation import transform_Q
from modules.abd_matrix import compute_ABD


def compute_laminate_response(material, stacking_sequence, ply_thickness, loads):
    """
    Compute strain and stress in each ply

    Parameters
    ----------
    material : dict
    stacking_sequence : list
    ply_thickness : float
    loads : list
        [Nx, Ny, Nxy, Mx, My, Mxy]

    Returns
    -------
    results : list of dict
    """

    A,B,D = compute_ABD(material, stacking_sequence, ply_thickness)

    ABD = np.block([
        [A, B],
        [B, D]
    ])

    load_vector = np.array(loads)

    ABD_inv = np.linalg.inv(ABD)

    strain_curvature = ABD_inv @ load_vector

    epsilon0 = strain_curvature[0:3]
    kappa = strain_curvature[3:6]

    n = len(stacking_sequence)
    total_thickness = n * ply_thickness

    z = np.linspace(-total_thickness/2, total_thickness/2, n+1)

    Q = reduced_stiffness_matrix(material)

    results = []

    for k in range(n):

        theta = stacking_sequence[k]

        Q_bar = transform_Q(Q, theta)

        z_mid = (z[k] + z[k+1]) / 2

        strain = epsilon0 + z_mid * kappa

        stress = Q_bar @ strain

        results.append({
            "ply": k+1,
            "angle": theta,
            "z": z_mid,
            "strain": strain,
            "stress": stress
        })

    return results
