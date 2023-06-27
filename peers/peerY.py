import socket, os, threading

# Definindo a porta e ip do servidor de acordo como o enunciado
server_port = 1099
server_ip = '127.0.0.1'
# Cria o Socket para a comunicacao peer e servidor
peer_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_server_socket.connect((server_ip, server_port))
peer_ip, peer_port = peer_server_socket.getsockname()

# Diretorios default para facilitar os testes em desenvolvimento
diretorio_peer = "directoryY/"
diretorio_peer_conectado = "directoryX/"
peer_escolhido_port = input("Defina a porta do peer: ")
# diretorio_peer_escolhido = input("Defina o diretorio do peer: ")
peer_socket_download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_socket_download.bind(('', int(peer_escolhido_port)))

def listPeerFiles(diretorio):
    list_files = os.listdir(diretorio)
    return list_files

# Funcao responsavel por ter como entrada o arquivo e escolher de qual peer deseja realizar o download do arquivo
def enviaOperacaoServidor(peer_server_socket, arquivo_download):
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_download = []
    mensagem_download.append("DOWNLOAD")
    ## enviar para o servidor tambem o nome do arquivo que deseja baixar
    mensagem_download.append(arquivo_download)
    peer_server_socket.send(str(mensagem_download).encode())
    peers_list_download = peer_server_socket.recv(1024).decode()
    print("Peers com arquivo para download: " + peers_list_download)


def join(peer_ip, peer_port, peer_server_socket, diretorio):
    # diretorio0 = input("Defina um diretorio para o peer: ")
    lista_arquivos = listPeerFiles(diretorio)

    # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
    mensagem_join = []
    mensagem_join.append("JOIN")
    mensagem_join.append(lista_arquivos)
    ## MANDAR A OPERACAO JOIN E A LISTA PARA O SERVIDOR
    peer_server_socket.send(str(mensagem_join).encode())
    if peer_server_socket.recv(1024).decode() == "JOIN_OK":
        print(">>> Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + ", ".join(lista_arquivos))



def search(peerSocket):
    arquivo = input("Arquivo a ser buscado: ")
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_search = []
    mensagem_search.append("SEARCH")
    mensagem_search.append(arquivo)
    peerSocket.send(str(mensagem_search).encode())

    peers_list = peerSocket.recv(2048).decode()
    print(">>> peers com arquivo solicitado: " + peers_list)


def menuOperacoes():
    operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")
    return operacao

class MenuThread(threading.Thread):
    def __init__(self, diretorio):
        threading.Thread.__init__(self)
        self.diretorio = diretorio

    def run(self):

        while True:
            operacao = menuOperacoes()

            ## JOIN OPERATION
            if operacao == '1':
                ## SO ABRIR A CONEXAO COM O SERVIDOR AO ENTRAR EM CADA OPERACAO
                # peer_ip, peer_port = abrirConexaoServidor(peer_server_socket)
                # peer_class = Peer(peer_ip, peer_port, self.diretorio)
                join(peer_ip, peer_port, peer_server_socket, self.diretorio)

            ## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
            elif operacao == '2':
                # abrirConexaoServidor(peer_server_socket)
                search(peer_server_socket)

            elif operacao == '3':
                arquivo_download = input("Arquivo que deseja realizar o download: ")
                # Peer x: ip e porta
                # peer Y: peer_escolhido_ip, peer_escolhido_port
                enviaOperacaoServidor(peer_server_socket, arquivo_download)

                # Aceita a conexao e inicia a thread de download
                ## Iniciar uma thread somente para rodar o download a parte
                thread_download = DownloadThread(arquivo_download)
                thread_download.start()


menu_thread = MenuThread(diretorio_peer)
## Iniciar uma thread somente para rodar o menu a parte
menu_thread.start()


# PEER Y RECEBER O NOME DO ARQUIVO E ENVIA O ARQUIVO PARA O PEER X
def aceitarReceberP2PNomeArquivo(peer_socket_download):
    peer_socket_download.listen(5)
    while True:
        #Accept para comecar a receber informacao do outro Peer para decode
        peer_req_download_socket, peer_req_download_address = peer_socket_download.accept()
        data = peer_req_download_socket.recv(1024)
        #recebe o nome do arquivo
        nome_arquivo = data.decode()
        print("nome_arquivo: " + nome_arquivo)
        # verificar se o arquivo existe
        path_arquivo = diretorio_peer_conectado + "/" + nome_arquivo
        print("path_arquivo "+ path_arquivo)
        if os.path.exists(path_arquivo):
            print("EXISTE")
            # abrir o arquivo e envia para o outro peer
            with open(path_arquivo, "rb") as file:
                chunk = file.read(1024)
                while chunk:
                    # Send the chunk to the server
                    peer_req_download_socket.send(chunk)
                    chunk = file.read(1024)
        peer_req_download_socket.close()

aceitarReceberP2PNomeArquivo(peer_socket_download)

def abrirConexaoPeerDownload(peer_escolhido_ip, peer_escolhido_port):
    try:
        peer_socket_download = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Inicializando/Conectando Peer Socket Download
        peer_socket_download.connect((peer_escolhido_ip, int(peer_escolhido_port)))
        return peer_socket_download
    except ConnectionRefusedError:
        print(f'Peer {peer_escolhido_ip}:{peer_escolhido_port} recusou a conexão')




# Como serao multiplos peers, vamos criar uma classe para configuracao desse Peer
class Peer():
    ## Cada peer tem o ip, porta e seu respectivo diretorio
    def __init__(self, peer_ip, peer_port, diretorio):
        self.peer_ip = peer_ip
        self.peer_port = peer_port
        self. diretorio = diretorio



# Como ja teremos uma thread para o menu se conectando ao servidor, teremos que ter outra thread pra rodar o download a parte
class DownloadThread(threading.Thread):

    def __init__(self, arquivo_download):
        threading.Thread.__init__(self)
        # self.peer_class = peer_class
        self.arquivo_download = arquivo_download

    def run(self):
        # Receber o arquivo_download e verificar que existe pra fazer o download e iniciar a transferencia
        receberArquivo(self.arquivo_download, diretorio_peer, peer_escolhido_port)



# Receber o arquivo_download e verificar que existe pra fazer o download e iniciar a transferencia
# PEER X RECEBER O ARQUIVO E ESCREVE NO DIRETORIO
def receberArquivo(nome_arquivo, diretorio_peer, peer_escolhido_port):
    socket_receber = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # CONECTA NO PEER ESCOLHIDO - peer y
    socket_receber.connect(('127.0.0.1', int(peer_escolhido_port)))

    # Abrindo um novo arquivo para escrever o conteudo recebido
    with open(diretorio_peer, "wb") as file:
        while True:
            # receber dados do peer que funciona como servidor e possui o arquivo
            chunk = socket_receber.recv(1024)
            if not chunk:
                # No more data, break the loop
                break
            # Write the received data to the file
            file.write(chunk)
    print("Arquivo " + nome_arquivo + " baixado com sucesso na pasta /" + diretorio_peer)
    socket_receber.close()
