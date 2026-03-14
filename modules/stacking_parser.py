import re


def parse_stacking_sequence(seq):
    """
    Parse laminate stacking notation.

    Examples
    --------
    [0/45/-45/90]s
    [0/90]2s
    [45/-45]4
    """

    seq = seq.replace(" ", "")

    symmetric = seq.endswith("s")

    if symmetric:
        seq = seq[:-1]

    match = re.match(r"\[(.*?)\](\d*)", seq)

    if not match:
        raise ValueError("Invalid stacking sequence format")

    inside = match.group(1)
    repeat = match.group(2)

    angles = [float(a) for a in inside.split("/")]

    if repeat:
        angles = angles * int(repeat)

    if symmetric:
        mirror = angles[::-1]
        angles = angles + mirror

    return angles
