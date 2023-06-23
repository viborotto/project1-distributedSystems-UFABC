import socket, os, threading

def listPeerFiles(diretorio):
    list_files = os.listdir(diretorio)
    return list_files

def join(peer_ip, peer_port, peerSocket, diretorio):
    # diretorio0 = input("Defina um diretorio para o peer: ")
    lista_arquivos = listPeerFiles(diretorio)

    # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
    mensagem_join = []
    mensagem_join.append("JOIN")
    mensagem_join.append(lista_arquivos)
    ## MANDAR A OPERACAO JOIN E A LISTA PARA O SERVIDOR
    peerSocket.send(str(mensagem_join).encode())
    print("Enviada mensagem com OPERACAO JOIN: " + str(mensagem_join))
    if peerSocket.recv(1024).decode() == "JOIN_OK":
        print(">>> Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + ", ".join(lista_arquivos))
    fecharConexaoServidor(peerSocket)

def search(peerSocket):
    arquivo = input("Arquivo a ser buscado: ")
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_search = []
    mensagem_search.append("SEARCH")
    mensagem_search.append(arquivo)
    peerSocket.send(str(mensagem_search).encode())
    peers_list = peerSocket.recv(2048).decode()
    print(">>> peers com arquivo solicitado: " + peers_list)
    fecharConexaoServidor(peerSocket)

# TODO: implementar download
def download(peerSocket):
    arquivo = input("Arquivo a ser buscado: ")
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_search = []
    mensagem_search.append("SEARCH")
    mensagem_search.append(arquivo)
    peerSocket.send(str(mensagem_search).encode())
    peers_list = peerSocket.recv(2048).decode()
    print(">>> peers com arquivo solicitado: " + peers_list)
    fecharConexaoServidor(peerSocket)

## TODO: cada operacao solicitada precisamos abrir conexao com o servidor(somente nesse momento)
def processaOperacao(peer_ip, peer_port, peerSocket, diretorio):
    while True:
        operacao = menuOperacoes()
            ## JOIN OPERATION
        if operacao == '1':
            join(peer_ip, peer_port, peerSocket, diretorio)

        ## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
        elif operacao == '2':
            search(peerSocket)

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


# Como serao multiplos peers, vamos criar uma classe para configuracao desse Peer
class Peer():
    ## Cada peer tem o ip, porta e seu respectivo diretorio
    def __init__(self, peer_ip, peer_port, diretorio):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self. diretorio = diretorio
        ## quando recebe o ip e porta do peer definido para que haja o donwload cria outro socket agindo como servidor
        # self.download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.download_socket.bind((self.peer_ip, self.peer_port))
        # self.download_socket.listen(5)

def abrirConexaoServidor(server_ip, server_port):
    peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Inicializando/Configurando Peer Socket Server
    peer_server_socket.connect((server_ip, server_port))
    return peer_server_socket

def fecharConexaoServidor(peer_server_socket):
    peer_server_socket = socket.socket()
    peer_server_socket.close()


def abrirConexaoPeerDownload(peer_ip, peer_port):
    peer_socket_download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Inicializando/Configurando Peer Socket Download
    peer_socket_download.connect((peer_ip, peer_port))
    return peer_socket_download

def menuOperacoes():
    operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")
    return operacao

# def peerAsServerDownload(peer_class):
#     while True:
#         # Fica espeprando para aceitar ate o outro peer conectar ao socket
#         peer_socket_as_server, peer_address_as_server = self.download_socket.accept()
#         # Como ja temos uma thread rodando com o menu e se conectando o peer ao servidor como Client da request, criaremos outra thread para o tratamento do download a parte
#         thread_download = self.DownloadThread()
#         thread_download.start()

class MenuThread(threading.Thread):
    def __init__(self, peerClass, peer_ip, peer_port, peerSocket, diretorio):
        threading.Thread.__init__(self)
        self.peerClass = peerClass
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self.diretorio = diretorio
        self.peerSocket = peerSocket

    def run(self):
        while True:
            operacao = menuOperacoes()
            ## JOIN OPERATION
            if operacao == '1':
                join(self.peer_ip, self.peer_port, self.peerSocket, self.diretorio)

            ## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
            elif operacao == '2':
                search(self.peerSocket)

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
                self.peerSocket.send(operacao.encode())
                break


# Como ja teremos uma thread para o menu se conectando ao servidor, teremos que ter outra thread pra rodar o download a parte
# class DownloadThread(threading.Thread):
#     def __init__(self, peer_class, peer_address, peer_socket):
#         threading.Thread.__init__(self)
#         self.peer_class = peer_class
#         self.peer_address = peer_address
#         self.peer_socket = peer_socket
#
#     def run(self):

def main():
        # define the port on which you want connect
        # nesse caso a porta que definimos no servidor
        server_port = 1099
        server_ip = '127.0.0.1'
        diretorio_peer = "directoryZ"

        peer_server_socket = abrirConexaoServidor(server_ip, server_port)
        address = peer_server_socket.getsockname()
        peer_ip, peer_port = peer_server_socket.getsockname()
        peer_class = Peer(peer_ip, peer_port, diretorio_peer)
        menu_thread = MenuThread(peer_class, peer_ip, peer_port, peer_server_socket, diretorio_peer)
        ## Iniciar uma thread somente para rodar o menu a parte
        menu_thread.start()

        ## Iniciar uma thread somente para rodar o download a parte




if __name__ == '__main__':
    main()