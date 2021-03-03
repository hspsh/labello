"""
Macros for EPL2 commands
"""

import qrcode
from math import ceil


def qr(x, y, data, box_size=3, border=0):
    _qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    _qr.add_data(data)
    _qr.make(fit=True)
    img = _qr.make_image()
    # img.show()
    pixels = list(img.getdata())
    w, h = img.size
    wb = ceil(w / 8) * 8

    result = "GW{},{},{},{}\n".format(x, y, wb // 8, h).encode()
    for row in range(h):
        f = lambda b: "0" if b == 0 else "1"
        offset = row * w
        bits = "".join([f(b) for b in pixels[offset : offset + w]]).ljust(wb, "1")
        ba = bytearray([int(bits[i : i + 8], 2) for i in range(0, len(bits), 8)])
        result += ba
    result += b"\n"

    return result.decode("ISO-8859-1")
