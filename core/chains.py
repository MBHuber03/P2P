import subprocess, time
from core.utils import runCmd

def iniciarHost(path):
    subprocess.Popen(["./freechains-host", "start", f"{path}"])
    time.sleep(1)

def pararHost():
    runCmd(f"./freechains-host stop")

def criarPubPvt(passphrase):
    output = runCmd(f"./freechains keys pubpvt '{passphrase}'").split()
    return (output[0], output[1]) # Pub, Pvt

def joinChain(chain, pub):
    try:
        return runCmd(f"./freechains chains join '{chain}' '{pub}'")
    except subprocess.CalledProcessError:
        print(f"Você já está na chain {chain}")
