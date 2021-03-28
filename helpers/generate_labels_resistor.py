e12 = [   10,    12,    15,    18,    22,    27,    33,    39,    47,    56,    68,    82,]
e6 = [10, 15, 22, 33, 47, 68]

def resistors():
    for v in e12:
        rv = tuple(round((v * (10 ** r)), 1) for r in range(-1, 2))
        print("[R] {} ohm; {} ohm; {} ohm".format(*rv))
        print("[R] {} Kohm; {} Kohm; {} Kohm".format(*rv))
        print("[R] {0} Mohm; {1} Mohm; {1}? ohm".format(*rv))

def caps():
    for v in e6:
        rv = tuple(round((v * (10 ** r)), 1) for r in range(-1, 2))
        rv = (*rv[1:], rv[0])
        print("[C] {} pF; {} pF; {} nF".format(*rv))
        print("[C] {} nF; {} nF; {} uF".format(*rv))
        print("[C] {} uF; {} uF; {} uF".format(rv[0], rv[1], rv[0]*100))

caps()

