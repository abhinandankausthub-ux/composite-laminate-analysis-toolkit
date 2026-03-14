import matplotlib.pyplot as plt
import numpy as np


def plot_laminate_stack(stacking_sequence, ply_thickness):
    """
    Plot laminate stacking sequence through thickness
    """

    n = len(stacking_sequence)

    total_thickness = n * ply_thickness

    z = np.linspace(-total_thickness/2, total_thickness/2, n+1)

    fig, ax = plt.subplots(figsize=(4,6))

    for i, angle in enumerate(stacking_sequence):

        z_bot = z[i]
        z_top = z[i+1]

        ax.fill_between(
            [0,1],
            z_bot,
            z_top,
            color="steelblue",
            alpha=0.8
        )

        ax.text(
            0.5,
            (z_bot + z_top) / 2,
            f"{angle}°",
            ha="center",
            va="center",
            fontsize=12,
            color="white",
            weight="bold"
        )

    ax.set_xlim(0,1)
    ax.set_ylim(-total_thickness/2, total_thickness/2)

    ax.set_xticks([])

    ax.set_ylabel("Thickness (z)")
    ax.set_title("Laminate Stacking Sequence")

    ax.grid(True, axis="y", linestyle="--", alpha=0.4)

    plt.tight_layout()

    return fig



def plot_stress_through_thickness(results):
    """
    Plot σx, σy, τxy through laminate thickness
    """

    z = []
    sigma_x = []
    sigma_y = []
    tau_xy = []

    for ply in results:

        z.append(ply["z"])

        stress = ply["stress"]

        sigma_x.append(stress[0])
        sigma_y.append(stress[1])
        tau_xy.append(stress[2])

    fig, ax = plt.subplots(figsize=(6,6))

    ax.plot(sigma_x, z, marker="o", label="σx")
    ax.plot(sigma_y, z, marker="s", label="σy")
    ax.plot(tau_xy, z, marker="^", label="τxy")

    ax.set_xlabel("Stress")
    ax.set_ylabel("Thickness (z)")

    ax.set_title("Stress Distribution Through Laminate")

    ax.legend()

    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    return fig
