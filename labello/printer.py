import subprocess


def get_status(printer=""):
    p = subprocess.Popen(args=["lpstat", "-p", printer], stdout=subprocess.PIPE)
    for line in iter(p.stdout.readline, b""):
        if printer in line.decode():
            return line.decode()
    return "failed"
