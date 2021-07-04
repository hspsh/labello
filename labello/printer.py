import subprocess

def get_status(printer=None):
    p = subprocess.Popen(args=["lpstat", "-p"],
        stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b''):
        if printer in line.decode():
            return line.decode()
    return "failed"