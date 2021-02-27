"""

dots w159h119
"""
import sys
import sqlite3
from itertools import cycle

from math import ceil

std_label = (160, 120)
thin_label = (140, 30)
label_size = thin_label

dpi = 203
w_dots = int(label_size[0] * dpi / 72)
h_dots = int(label_size[1] * dpi / 72)
label_rows = 1
h_row = h_dots // label_rows

h_offset = cycle(range(0, h_dots, h_row))


conn = sqlite3.connect("labels.db")
c = conn.cursor()

# Create table
c.execute(
    """CREATE TABLE IF NOT EXISTS labels
             (id INTEGER PRIMARY KEY AUTOINCREMENT, 
             text TEXT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)"""
)


buf = False
for no, line in enumerate(sys.stdin):
    # TODO: strip to ASCII only
    line = line.strip()
    _o_line = line

    mr = 0
    if line.startswith("["):
        drop_cap, line = line[1:].split("]")
        if len(drop_cap) == 1:
            mr = 2
        else:
            mr = len(drop_cap)
    else:
        drop_cap = None
#    chw = 16 - mr
    chw = 16
    rows_in_line = ceil(len(line) / chw)
#    print(len(line), rows_in_line)

    h0 = next(h_offset)
    if no % label_rows == 0:
        print("N")
        print("q" + str(w_dots))
        buf = True
    else:
        print("LO", end="")
        print(0, h0, w_dots, 1, sep=",")

    c.execute("INSERT INTO labels (text) VALUES (?)", (_o_line,))
    id = c.lastrowid

    if rows_in_line == 1:
        print("A", end="")
        print(
            10,
            h0 + 10,
            0,
            4,
            2 if len(line) < (chw // 2) else 1,
            3,
            "N",
            '"{}"'.format(line[:chw]),
            sep=",",
        )

    elif rows_in_line == 2:
        print("A", end="")
        print(
            10,
            h0 + 5,
            0,
            4,
            1,
            2,
            "N",
            '"{}"'.format(line[:chw]),
            sep=",",
        )
        print("A", end="")
        print(
            10,
            h0 + 5 + h_row // 2,
            0,
            4,
            1,
            1,
            "N",
            '"{}"'.format(line[chw : chw * 2]),
            sep=",",
        )

    elif rows_in_line == 3:
        print("A", end="")
        print(
            10,
            h0,
            0,
            4,
            1,
            1,
            "N",
            '"{}"'.format(line[:chw]),
            sep=",",
        )
        print("A", end="")
        print(
            10,
            h0 + h_row // 3,
            0,
            4,
            1,
            1,
            "N",
            '"{}"'.format(line[chw : chw * 2]),
            sep=",",
        )
        print("A", end="")
        print(
            10,
            h0 + (h_row // 3) * 2,
            0,
            4,
            1,
            1,
            "N",
            '"{}"'.format(line[chw * 2 : chw * 3]),
            sep=",",
        )

    if drop_cap:
        print("A", end="")
        print(
            10,
            h0,
            0,
            4,
            2 if len(drop_cap) < 2 else 1,
            3,
            "N",
            '"{}"'.format(drop_cap),
            sep=",",
        )

    print("B", end="")
    print(
        w_dots - 154,
        h0 + 5,
        0,  # postition, rotation
        "E80",
        2,
        6,  # barcode settings
        h_row - 20,  # height
        "B",  # human readable
        '"{:07d}"'.format(id),  # data 7 digit,
        sep=",",
    )

    if (no + 1) % label_rows == 0:
        print("P1")
        buf = False
if buf:
    print("P1")

conn.commit()
conn.close()
