import subprocess

def runCmd(command):
    # Executa um comando e retorna a saída.
    output = subprocess.check_output(command, shell=True, text=True)
    return output.strip()

def likeMensagem(chain, idProduto):
    return runCmd(f"freechains chain {chain} like {idProduto}")

def dislikeMensagem(chain, idProduto):
    return runCmd(f"freechains chain {chain} dislike {idProduto}")

