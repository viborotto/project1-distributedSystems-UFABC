import socket, os
#FUNC PEERS; JOIN, SEARCH, UPDATE, DOWNLOAD

s = socket.socket()
file_name = "arquivo.mp4"

# define the port on which you want connect
# nesse caso a porta que definimos no servidor
server_port = 1099
server_ip = '127.0.0.1'

s.connect((server_ip, server_port))
address = s.getsockname()
peer_ip, peer_port = s.getsockname()
diretorio = "directoryX"

def listPeerFiles():
    list_files = os.listdir(diretorio)
    return list_files

while True:
    operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")
        ## JOIN OPERATION
    if operacao == '1':
        # diretorio0 = input("Defina um diretorio para o peer: ")
        lista_arquivos = listPeerFiles()

        # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
        mensagem_join = []
        mensagem_join.append("JOIN")
        mensagem_join.append(lista_arquivos)
        ## MANDAR A OPERACAO JOIN E A LISTA PARA O SERVIDOR
        s.send(str(mensagem_join).encode())
        print("Enviada mensagem com OPERACAO JOIN: "+ str(mensagem_join))
        if s.recv(1024).decode() == "JOIN_OK":
            print(">>> Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + ", ".join(lista_arquivos))

    ## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
    elif operacao == '2':
        arquivo = input("Arquivo a ser buscado: ")
        ## Manda operacao e qual o arquivo o servidor deve buscar
        mensagem_search = []
        mensagem_search.append("SEARCH")
        mensagem_search.append(arquivo)
        s.send(str(mensagem_search).encode())
        peers_list = s.recv(2048).decode()
        print(">>> peers com arquivo solicitado: " + peers_list)

    elif operacao == '3':
        arquivo = input("Arquivo que deseja realizar o download: ")
        mensagem_download = []
        mensagem_download.append("DOWNLOAD")
        ## enviar para o servidor tambem o nome do arquivo que deseja baixar
        mensagem_download.append(arquivo)
        s.send(str(mensagem_download).encode())
        # TODO: print("Arquivo "+ arquivo+ " baixado com sucesso na pasta /"+ diretorio)
        peers_list_download = s.recv(2048).decode()
        print("Peers com arquivo para download: " + peers_list_download)
        peer_escolhido = input("Escolha o Peer que deseja realizar o download do arquivo: ")
        # TODO: PeerX deve requisitar o arquivo para o peer_escolhido, por exemplo PeerY
        ## PeerY podera aceitar ou negar o pedido
        ## PeerY aceitando o pedido, peerX baixara o arquivo na pasta directoryX


    elif operacao == 'quit':
        s.send(operacao.encode())
        break

s.close()
