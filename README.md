# P2P-CompraVenda
Protótipo de uma rede peer-to-peer de compra e venda de produtos utilizando o protocolo do Freechains.

# Objetivo:
O objetivo da aplicação criada é a compra e venda de produtos pelos usuários. 

# Requerimentos:
1. É necessário ter o Freechains instalado no sistema.
2. O protótipo deve ser executado no mesmo diretório do Freechains.

# Interação:
1. O usuário deve fornecer uma senha para gerar suas chaves pública e privada.
2. O usuário deve escolher uma das opções do menu para interagir com a rede:
  - Criar anúncio: o usuário deverá fornecer os dados do produto pedidos pelo sistema para que seja postado na rede.
  - Listar anúncios: o sistema irá apresentar os anúncios da rede e suas informações.
  - Comprar produto: o usuário deverá fornecer o ID do bloco do anúncio que deseja comprar, além de outros dados da compra pedidos pelo sistema.
  - Confirmar compra: o sistema irá listar os pedidos pendentes feitos por outros usuários. O usuário deve escolher um dos pedidos e escolher se aceita ou rejeita o pedido.
  - Sair: o programa é terminado.

# Ferramentas:
1. Comando do freechains para postagem de conteúdo.
2. Comando do freechains para geração de chaves pub e pvt.
3. Comando consensus do freechains para listar anúncios e pedidos pendentes e calcular o estoque de um produto.
4. Comando payload do freechains para obter o conteúdo dos blocos.
