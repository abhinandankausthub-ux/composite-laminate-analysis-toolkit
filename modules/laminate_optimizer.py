import itertools

from modules.ply_stress import compute_laminate_response
from modules.failure_criteria import tsai_hill_failure


def optimize_laminate(material, ply_thickness, loads):

    candidate_angles = [0,45,-45,90]

    best_stack = None
    best_fi = 1e9

    for combo in itertools.product(candidate_angles, repeat=4):

        stack = list(combo) + list(combo[::-1])

        results = compute_laminate_response(
            material,
            stack,
            ply_thickness,
            loads
        )

        max_fi = 0

        for ply in results:

            FI = tsai_hill_failure(ply["stress"], material)

            max_fi = max(max_fi, FI)

        if max_fi < best_fi:

            best_fi = max_fi
            best_stack = stack

    return best_stack, best_fi
