import json, os
from core.utils import runCmd
from core.compra import calcularEstoqueAtual

def criarAnuncio(chain, pub, pvt):
    titulo = input("Título do produto: ")
    descricao = input("Descrição do produto: ")
    preco = input("Preço: ")
    quantidade = int(input("Quantidade disponível: "))

    anuncio = {
        "tipo": "anuncio",
        "titulo": titulo,
        "descriao": descricao,
        "preco": preco,
        "quantidade": quantidade,
        "vendedor": pub,
    }

    with open("temp.json", "w") as f:
        json.dump(anuncio, f)

    cmd = f"./freechains chain '{chain}' post file 'temp.json' --sign='{pvt}'"
    postID = runCmd(cmd)
    os.remove("temp.json")

    print(f"Anúncio criado com ID: {postID})")

def listarAnuncios(chain):
    posts = runCmd(f"./freechains chain '{chain}' consensus").split()
    for pid in posts:
        content = runCmd(f"./freechains chain '{chain}' get payload '{pid}'")
        print(f"\nID: {pid}\n'{content}'")

def avaliarAnuncio():
    idProduto = input("ID do produto para avaliar: ")
    op = input("Like (1) ou Dislike (2)? ")

    if op == "1":
        likeMensagem(chain, idProduto)
        print("Curtido.")
    elif op == "2":
        dislikeMensagem(chain, idProduto)
        print("Não curtido.")
    else:
        print("Opção inválida.")
