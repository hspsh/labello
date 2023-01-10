"""
Macros for EPL2 commands
"""

import qrcode
import math


import qrcode
import math

def qr(x, y, data, box_size=3, border=0):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    pixels = img.getdata()
    width, height = img.size
    width_bytes = math.ceil(width / 8) * 8

    result = f"GW{x},{y},{width_bytes // 8},{height}\n"
    for row in range(height):
        bits = ''.join('1' if pixel else '0' for pixel in pixels[row*width : (row+1)*width]).ljust(width_bytes, '1')
        bytes = bytes([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
        result += bytes.decode()
    result += '\n'

    return result.decode("ISO-8859-1")
