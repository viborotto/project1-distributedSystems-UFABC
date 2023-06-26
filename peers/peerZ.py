import socket, os, threading, time
import logging
logger = logging.getLogger('ftpuploader')

# define the port on which you want connect
# nesse caso a porta que definimos no servidor
server_port = 1099
server_ip = '127.0.0.1'
#cria o Socket mas nao conecta ainda ao servidor, só vamos conectar ao entrar na operacao
peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listPeerFiles(diretorio):
    list_files = os.listdir(diretorio)
    return list_files

def abrirConexaoServidor(peer_server_socket):
        peer_server_socket.connect((server_ip, server_port))
        peer_ip, peer_port = peer_server_socket.getsockname()
        return peer_ip, peer_port

    # else:
    #     print("Peer ja conectado ao servidor")



def fecharConexaoServidor(peer_server_socket):
    print("Conexao fechada com o servidor")
    peer_server_socket.close()


def abrirConexaoPeerDownload(peer_ip, peer_port):
    peer_socket_download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Inicializando/Configurando Peer Socket Download
    peer_socket_download.connect((peer_ip, peer_port))
    return peer_socket_download


def menuOperacoes():
    operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")
    return operacao


def join(peer_ip, peer_port, peer_server_socket, diretorio):
    # diretorio0 = input("Defina um diretorio para o peer: ")
    lista_arquivos = listPeerFiles(diretorio)

    # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
    mensagem_join = []
    mensagem_join.append("JOIN")
    mensagem_join.append(lista_arquivos)
    ## MANDAR A OPERACAO JOIN E A LISTA PARA O SERVIDOR
    peer_server_socket.send(str(mensagem_join).encode())
    print("Enviada mensagem com OPERACAO JOIN: " + str(mensagem_join))
    if peer_server_socket.recv(1024).decode() == "JOIN_OK":
        print(">>> Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + ", ".join(lista_arquivos))

    # FECHA CONEXAO COM SERVIDOR
    fecharConexaoServidor(peer_server_socket)

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



# Como serao multiplos peers, vamos criar uma classe para configuracao desse Peer
class Peer():
    ## Cada peer tem o ip, porta e seu respectivo diretorio
    def __init__(self, peer_ip, peer_port, diretorio):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self. diretorio = diretorio



class MenuThread(threading.Thread):
    def __init__(self, diretorio):
        threading.Thread.__init__(self)
        self.diretorio = diretorio

    def run(self):

        while True:
            operacao = menuOperacoes()

            if operacao == 'quit':
                abrirConexaoServidor(peer_server_socket)
                peer_server_socket.send(operacao.encode())
                break

            ## JOIN OPERATION
            elif operacao == '1':
                ## SO ABRIR A CONEXAO COM O SERVIDOR AO ENTRAR EM CADA OPERACAO
                peer_ip, peer_port = abrirConexaoServidor(peer_server_socket)
                peer_class = Peer(peer_ip, peer_port, self.diretorio)
                join(peer_ip, peer_port, peer_server_socket, self.diretorio)
                print("Fim JOIN, PEER PRONTO PARA NOVA OPERACAO")

            ## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
            elif operacao == '2':
                abrirConexaoServidor(peer_server_socket)
                search(peer_server_socket)
                print("Fim SEARCH, PEER PRONTO PARA NOVA OPERACAO")

            elif operacao == '3':
                peer_ip, peer_port = abrirConexaoServidor(peer_server_socket)
                # Cria socket como servidor para processar o download
                download_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                download_socket.bind((peer_ip, peer_port))
                download_socket.listen(5)
                print("PeerZ socket is listening")


                # TODO: PeerX deve requisitar o arquivo para o peer_escolhido, por exemplo PeerY
                # De acordo com o peer escolhido iremos abrir uma conexao com o Peer definido para que haja o download
                # Abre a conexao mas tem que receber uma mensagem 'yes' pra continuar
                downloadInfos(peer_server_socket)
                # Aceita a conexao e inicia a thread de download
                # peerAsServerDownload(download_socket)

                ## PeerY podera aceitar ou negar o pedido
                ## como o peerY vai receber que o peerX ta solicitando um arquivo?
                # PeerY aceitando o pedido, peerX baixara o arquivo na pasta directoryX
                # if peerSocket.recv(2048).decode() == "yes":
                #     print("yees pronto para realizar o download em PeerX")
                download_socket.close()


def peerAsServerDownload(download_socket):
    while True:
        # Fica espeprando para aceitar ate o outro peer conectar ao socket
        # Estabilish connection with client
        peer_download_socket, peer_download_address = download_socket.accept()
        # Como ja temos uma thread rodando com o menu e se conectando o peer ao servidor como Client da request, criaremos outra thread para o tratamento do download a parte
        ## Iniciar uma thread somente para rodar o download a parte
        thread_download = DownloadThread()
        thread_download.start()

# TODO: implementar downloadtHREAD E METODO
# Como ja teremos uma thread para o menu se conectando ao servidor, teremos que ter outra thread pra rodar o download a parte
class DownloadThread(threading.Thread):

    def __init__(self):
    # def __init__(self, peer_class, peer_address, peer_socket):
        threading.Thread.__init__(self)
        # self.peer_class = peer_class
        # self.peer_address = peer_address
        # self.peer_socket = peer_socket

    def run(self):
        print("ACAO DE DOWNLOAD A SER IMPLEMENTADA")


# TODO: print("Arquivo "+ arquivo+ " baixado com sucesso na pasta /"+ diretorio)
# Funcao responsavel por ter como entrada o arquivo e escolher de qual peer deseja realizar o download do arquivo
def downloadInfos(peer_server_socket):
    arquivo = input("Arquivo que deseja realizar o download: ")
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_download = []
    mensagem_download.append("DOWNLOAD")
    ## enviar para o servidor tambem o nome do arquivo que deseja baixar
    mensagem_download.append(arquivo)
    peer_server_socket.send(str(mensagem_download).encode())
    peers_list_download = peer_server_socket.recv(1024).decode()
    print("Peers com arquivo para download: " + peers_list_download)

    # quando recebe o ip e porta do peer definido para que haja o donwload cria outro socket agindo como servidor
    peer_escolhido = input("Escolha o Peer que deseja realizar o download do arquivo: ")
    peer_escolhido_ip, peer_escolhido_port = peer_escolhido.split(':')
    print("peer_escolhido_ip: " + peer_escolhido_ip)
    print("peer_escolhido_port: " + peer_escolhido_port)
    abrirConexaoPeerDownload(peer_escolhido_ip, peer_escolhido_port)
        # TODO: Chamar a funcao de donwloadArquivo
    # downloadArquivo()

    fecharConexaoServidor(peer_server_socket)

def downloadArquivo(socket, nome_arquivo, tamanho_arquivo, diretorio):
    print("download_arquivo func")
    #TODO: implementar logica de download

def main():
        diretorio_peer = "directoryZ"
        menu_thread = MenuThread(diretorio_peer)
        ## Iniciar uma thread somente para rodar o menu a parte
        menu_thread.start()


if __name__ == '__main__':
    main()