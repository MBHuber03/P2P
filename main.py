from core.chains import iniciarHost, criarPubPvt, joinChain, pararHost
from core.anuncio import criarAnuncio, listarAnuncios, avaliarAnuncio
from core.compra import comprarProduto, confirmarCompra
from core.utils import runCmd
import os, config, json

def preparar_ambiente_de_teste(chain, admin_pub, admin_pvt):
    anuncios = [
        {"titulo": "Camiseta", "descricao": "Camiseta 100% algodão", "preco": "50", "quantidade": 10},
        {"titulo": "Fone de Ouvido", "descricao": "Bluetooth, 10h duração", "preco": "150", "quantidade": 5},
        {"titulo": "Livro Python", "descricao": "Curso completo de Python", "preco": "80", "quantidade": 7},
    ]

    for a in anuncios:
        anuncio = {
            "tipo": "anuncio",
            "titulo": a["titulo"],
            "descriao": a["descricao"],
            "preco": a["preco"],
            "quantidade": a["quantidade"],
            "vendedor": admin_pub,
        }

        with open("temp.json", "w") as f:
            json.dump(anuncio, f)

        cmd = f"./freechains chain '{chain}' post file 'temp.json' --sign='{admin_pvt}'"
        postID = runCmd(cmd)

        print(f"Anúncio '{a['titulo']}' criado com ID: {postID}")

    os.remove("temp.json")

def menu():
    while True:
        print("\nMercado P2P")
        print("1. Criar anúncio")
        print("2. Listar anúncios")
        print("3. Comprar produto")
        print("4. Confirmar Compra")
        print("5. Sair")

        op = input("Escolha uma opção: ")
        if op == "1":
            criarAnuncio(config.chain, pub, pvt)
        elif op == "2":
            listarAnuncios(config.chain)
        elif op == "3":
            comprarProduto(config.chain, pub, pvt)
        elif op == "4":
            confirmarCompra(config.chain, pub, pvt)
        elif op == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

iniciarHost(config.path)
pub, pvt = criarPubPvt(config.passphrase)
joinChain(config.chain, pub)
preparar_ambiente_de_teste(config.chain, pub, pvt)
menu()
pararHost()
