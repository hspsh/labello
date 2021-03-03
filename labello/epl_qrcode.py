"""
QR Code support for EPL2
"""

import qrcode
from math import ceil

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=3,
    border=0,
)
qr.add_data('i.hsp.sh/00001')
qr.make(fit=True)
img = qr.make_image()
img.show()
pixels = list(img.getdata())
w, h = img.size

with open("qrcode.txt", "wb") as file:
    wb = ceil(w/8)*8
    file.write("""N
q812
S2
""".encode())
    file.write("GW100,100,{},{}\n".format(wb//8,h).encode())
    for row in range(h):
        f = lambda b: "0" if b == 0 else "1"
        offset = row*w
        
        bits = "".join([f(b) for b in pixels[offset:offset+w]]).ljust(wb, "1")
        ba = bytearray([int(bits[i:i+8], 2) for i in range(0, len(bits), 8)])
        print(ba)
        file.write(ba)
    file.write(b"\nP1\n\n")