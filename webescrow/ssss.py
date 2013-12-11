import os
import subprocess

import escrowcoins.settings as settings


def split(secret, n, m):
    cmd = settings.SSSS_SPLIT
    proc = subprocess.Popen([cmd, "-t", str(n), "-n", str(m), "-w", "s", "-q"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = proc.communicate(secret)
    shares = stdout.strip().split()
    return shares

