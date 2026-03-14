import numpy as np


def transform_Q(Q, theta_deg):
    """
    Transform lamina stiffness matrix Q into laminate coordinates.

    Parameters
    ----------
    Q : numpy array (3x3)
        Reduced stiffness matrix
    theta_deg : float
        Ply orientation angle (degrees)

    Returns
    -------
    Q_bar : numpy array (3x3)
        Transformed stiffness matrix
    """

    theta = np.radians(theta_deg)

    m = np.cos(theta)
    n = np.sin(theta)

    Q11 = Q[0,0]
    Q22 = Q[1,1]
    Q12 = Q[0,1]
    Q66 = Q[2,2]

    Qbar11 = Q11*m**4 + Q22*n**4 + 2*(Q12+2*Q66)*m**2*n**2
    Qbar22 = Q11*n**4 + Q22*m**4 + 2*(Q12+2*Q66)*m**2*n**2
    Qbar12 = (Q11+Q22-4*Q66)*m**2*n**2 + Q12*(m**4+n**4)

    Qbar16 = (Q11-Q12-2*Q66)*m**3*n - (Q22-Q12-2*Q66)*m*n**3
    Qbar26 = (Q11-Q12-2*Q66)*m*n**3 - (Q22-Q12-2*Q66)*m**3*n

    Qbar66 = (Q11+Q22-2*Q12-2*Q66)*m**2*n**2 + Q66*(m**4+n**4)

    Q_bar = np.array([
        [Qbar11, Qbar12, Qbar16],
        [Qbar12, Qbar22, Qbar26],
        [Qbar16, Qbar26, Qbar66]
    ])

    return Q_bar
