import numpy as np

from modules.ply_stress import compute_laminate_response
from modules.failure_criteria import tsai_hill_failure


def progressive_failure(material, stack, ply_thickness, loads, load_step=0.05, max_factor=5.0):

    """
    Progressive ply failure simulation using Tsai-Hill criterion.
    Load is increased gradually until plies fail.
    """

    failure_sequence = []
    failed_plies = set()

    load_factor = 1.0

    while load_factor <= max_factor:

        scaled_loads = [l * load_factor for l in loads]

        results = compute_laminate_response(
            material,
            stack,
            ply_thickness,
            scaled_loads
        )

        for ply in results:

            ply_id = ply["ply"]

            if ply_id in failed_plies:
                continue

            stress = ply["stress"]

            FI = tsai_hill_failure(stress, material)

            if FI >= 1.0:

                failed_plies.add(ply_id)

                failure_sequence.append({
                    "Ply": ply_id,
                    "Angle": ply["angle"],
                    "Load Factor": round(load_factor, 3)
                })

        if len(failed_plies) == len(stack):
            break

        load_factor += load_step

    return failure_sequence
