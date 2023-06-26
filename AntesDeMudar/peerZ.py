import socket, os

diretorio = "directoryZ"
# define the port on which you want connect
# nesse caso a porta que definimos no servidor
server_port = 1099
server_ip = '127.0.0.1'

# Inicializando/Configurando Peer Socket
peerSocket = socket.socket()
peerSocket.connect((server_ip, server_port))
address = peerSocket.getsockname()
peer_ip, peer_port = peerSocket.getsockname()

def listPeerFiles():
    list_files = os.listdir(diretorio)
    return list_files

def join():
    # diretorio0 = input("Defina um diretorio para o peer: ")
    lista_arquivos = listPeerFiles()

    # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
    mensagem_join = []
    mensagem_join.append("JOIN")
    mensagem_join.append(lista_arquivos)
    ## MANDAR A OPERACAO JOIN E A LISTA PARA O SERVIDOR
    peerSocket.send(str(mensagem_join).encode())
    print("Enviada mensagem com OPERACAO JOIN: " + str(mensagem_join))
    if peerSocket.recv(1024).decode() == "JOIN_OK":
        print(">>> Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + ", ".join(lista_arquivos))

def search():
    arquivo = input("Arquivo a ser buscado: ")
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_search = []
    mensagem_search.append("SEARCH")
    mensagem_search.append(arquivo)
    peerSocket.send(str(mensagem_search).encode())
    peers_list = peerSocket.recv(2048).decode()
    print(">>> peers com arquivo solicitado: " + peers_list)

def fecharConexao(socket):
    socket.close()

while True:
    operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")
        ## JOIN OPERATION
    if operacao == '1':
        join()

    ## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
    elif operacao == '2':
        search()

    elif operacao == '3':
        peer_solicitante_sock = socket.socket()
        arquivo = input("Arquivo que deseja realizar o download: ")
        mensagem_download = []
        mensagem_download.append("DOWNLOAD")
        ## enviar para o servidor tambem o nome do arquivo que deseja baixar
        mensagem_download.append(arquivo)
        peerSocket.send(str(mensagem_download).encode())

        peers_list_download = peerSocket.recv(2048).decode()
        print("Peers com arquivo para download: " + peers_list_download)

        peer_escolhido = input("Escolha o Peer que deseja realizar o download do arquivo: ")
        peer_escolhido_ip, peer_escolhido_port = peer_escolhido.split(':')
        print("peer_escolhido_ip: " + peer_escolhido_ip)
        print("peer_escolhido_port: " + peer_escolhido_port)

        # TODO: PeerX deve requisitar o arquivo para o peer_escolhido, por exemplo PeerY
        # De acordo com o peer escolhido iremos abrir uma conexao com o Peer definido para que haja o download
        peer_solicitante_sock.bind((peer_escolhido_ip, int(peer_escolhido_port)))
        print("peer_solicitante_sock binded to %s" % (peer_escolhido_port))
        peer_solicitante_sock.listen(5)
        print("PeerX socket is listening")
        # Estabilish connection with client, abre a conexao mas tem que receber uma mensagem 'yes' pra continuar
        peerSocket, peerAddress = peer_solicitante_sock.accept()

        ## PeerY podera aceitar ou negar o pedido
        ## como o peerY vai receber que o peerX ta solicitando um arquivo?
        if peerSocket.recv(2048).decode() == "yes":
            ## todo: fazer download
            print("yees pronto para realizar o download em PeerX")



    # TODO: print("Arquivo "+ arquivo+ " baixado com sucesso na pasta /"+ diretorio)


        ## PeerY aceitando o pedido, peerX baixara o arquivo na pasta directoryX
        # if opcao == "yes":

    elif operacao == 'quit':
        peerSocket.send(operacao.encode())
        break

fecharConexao(peerSocket)
