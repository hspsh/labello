common_vals = [
    10,
    12,
    15,
    18,
    22,
    27,
    33,
    39,
    47,
    56,
    68,
    82,
]

for v in common_vals:
    rv = tuple(round((v * (10 ** r)), 1) for r in range(-1, 2))
    print("[R] {:>9} ohm {:>9} ohm {:>9} ohm".format(*rv))
    print("[R] {:>8}K ohm {:>8}K ohm {:>8}K ohm".format(*rv))
    print("[R] {0:>8}M ohm {1:>8}M ohm {1:>8}? ohm".format(*rv))
