import json, os
from core.utils import runCmd

def calcularEstoqueAtual(chain, produtoID):
    posts = runCmd(f"./freechains chain '{chain}' consensus").split()
    qtdInicial = 0
    compras = []
    confirmacoes = {}

    for pid in posts:
        content = runCmd(f"./freechains chain '{chain}' get payload '{pid}'")
        try:
            data = json.loads(content)
            if pid == produtoID:
                if data.get("tipo") == "anuncio":
                    qtdInicial = int(data.get("quantidade", 0))
                elif data.get("tipo") == "compra":
                    compras.append((pid, data))
                elif data.get("tipo") == "confirmacao":
                    confirmacoes[data.get("compraID")] = data.get("status")
        except:
            continue

    totalVendido = 0
    for pid, compra in compras:
        if confirmacoes.get(pid) == "aceito":
            totalVendido += int(compra.get("quantidade", 0))
    return qtdInicial - totalVendido

def registrarCompra(chain, produtoID, qtd, compradorPub, pvt):
    compra = {
        "tipo": "compra",
        "produtoID": produtoID,
        "comprador": compradorPub,
        "quantidade": qtd,
    }

    with open("tempCompra.json", "w") as f:
        json.dump(compra, f)

    cmd = f"./freechains chain '{chain}' post file 'tempCompra.json' --sign='{pvt}'"
    postID = runCmd(cmd)
    os.remove("tempCompra.json")

    print(f"Compra registrada com ID: '{postID}'")

def comprarProduto(chain, pub, pvt):
    produtoID = input("ID do produto: ")
    qtd = calcularEstoqueAtual(chain, produtoID)
    print(f"Quantidade disponível: {qtd}")

    if qtd <= 0:
        print("Produto esgotado!")
        return

    compraQtd = int(input("Quantidade desejada: "))
    if compraQtd <= 0 or compraQtd > qtd:
        print("Quantidade inválida or superior ao estoque")
        return
    
    registrarCompra(chain, produtoID, compraQtd, pub, pvt)

def listarComprasPendentesParaVendedor(chain, pub):
    posts = runCmd(f"./freechains chain '{chain}' consensus").split()
    
    anunciosDoUsuario = {}
    comprasPorProduto = {}
    confirmacoes = {}

    for pid in posts:
        try:
            content = runCmd(f"./freechains chain '{chain}' get payload '{pid}'")
            data = json.loads(content)
            tipo = data.get("tipo")

            if tipo == "anuncio" and data.get("vendedor") == pub:
                produtoID = pid
                anunciosDoUsuario[produtoID] = data

            elif tipo == "compra":
                produtoID = data.get("produtoID") 
                if produtoID not in comprasPorProduto:
                    comprasPorProduto[produtoID] = []
                comprasPorProduto[produtoID].append((pid, data))

            elif tipo == "confirmacao":
                confirmacoes[data.get("compraID")] = data.get("status")

        except:
            continue

    pendentes = []

    for produtoID, anuncio in anunciosDoUsuario.items():
        if produtoID in comprasPorProduto:
            for compraID, compra in comprasPorProduto[produtoID]:
                if confirmacoes.get(compraID) is None:
                    pendentes.append((compraID, anuncio, compra))

    return pendentes

def confirmarCompra(chain, pub, pvt):
    pendentes = listarComprasPendentesParaVendedor(chain, pub)

    if not pendentes:
        print("Nenhuma compra pendente para seus anúncios.")
        return

    # Mostra as compras pendentes
    print("\nCompras pendentes:\n")
    for i, (compraID, anuncio, compra) in enumerate(pendentes):
        print(f"[{i}] ProdutoID: {compra.get('produtoID')}")
        print(f"      Produto: {anuncio.get('titulo')} | Compra ID: {compra.get('compraID')}")
        print(f"      Comprador: {compra.get('comprador')}")
        print(f"      Quantidade: {compra.get('quantidade')}\n")

    # Seleciona uma compra para confirmar
    try:
        escolha = int(input("Escolha o número da compra que deseja confirmar: "))
        compraID, anuncio, compra = pendentes[escolha]
    except (IndexError, ValueError):
        print("Escolha inválida.")
        return

    # Confirmação ou rejeição
    status = input("Confirmar (1) ou Rejeitar (2)? ")
    if status == "1":
        status_text = "aceito"
    elif status == "2":
        status_text = "rejeitado"
    else:
        print("Opção inválida.")
        return

    confirmacao = {
        "tipo": "confirmacao",
        "compraID": compraID,
        "status": status_text,
        "vendedor": pub
    }

    with open("tempConfirmacao.json", "w") as f:
        json.dump(confirmacao, f)

    cmd = f"./freechains chain '{chain}' post file 'tempConfirmacao.json' --sign='{pvt}'"
    postID = runCmd(cmd)
    os.remove("tempConfirmacao.json")

    print(f"Confirmação registrada com ID: {postID}")
