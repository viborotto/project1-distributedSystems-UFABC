import socket, threading
import ast

# Estrutura de dados para armazenamento de informacoes Peers - Dicionario
# Key: "ipPeer:portaPeer"
# Value: lista de arquivos e.g: ["arquivo1.mp4", "arquivo2.mp4"]
dicionarioPeers = {}

def configurarServidor():
    port = 1099
    ip = "127.0.0.1"
    # Inicializando/Configurando Server Socket
    serverSocket = socket.socket()
    print("Server Socket EP1 created")
    serverSocket.bind((ip, port))
    print("server socket binded to %s" % (port))
    return serverSocket

def abrirConexaoServidor(server_socket):
    # Loop para ficar escutando a forever loop until or interrupt it or an error occurs
    # put socket into listening mode
    server_socket.listen(5)
    print("server socket is listening")


def fecharConexaoServidor(server_socket):
    server_socket.close()

def listening(server_socket):
    while True:
        # Estabilish connection with client
        peerSocket, peerAddress = server_socket.accept()
        print("Server Connection accepted")
        print("###########################")
        # Separando as informacoes em duas variaveis peer_ip e peer_port
        peer_ip, peer_port = peerAddress
        # inicializa uma thread de peer
        newthread = HandlePeerThread(peerAddress, peerSocket)
        newthread.start()

# Funcao para tratar a string recebida do peer, separando em uma lista com operacao e arquivos do peer
def ajustarMensagemRecebida(mensagem_recebida):
    ajustada = ast.literal_eval(mensagem_recebida)
    operacao = ajustada[0]
    informacoes_recebidas = ajustada[1]
    return ajustada, operacao, informacoes_recebidas


# Funcao para salvar as informacoes recebidas do peer em um dicionario
def salvarListaArquivos(key_dic, lista_arquivos_recebida):
    #dicionarioPeers = {"ip:port": ["arquivo1.txt", "arquivo2.txt"]}
    dicionarioPeers[key_dic] = lista_arquivos_recebida
    print("Peer " + key_dic + " adicionado com arquivos "+ ", ".join(dicionarioPeers[key_dic]))
    print(dicionarioPeers)


    ## Funcao para realizar busca na estrutura de dados e retornar lista vazia ou de peers
def buscarArquivo(nome_arquivo):
    listaPeers = []
    for key_dic, value in dicionarioPeers.items():
        print("Peer " + key_dic + " solicitou arquivo " + nome_arquivo)
        for file in value:
            if file == nome_arquivo:
                listaPeers.append(key_dic)
    return listaPeers


def operacaoJoin(informacoes_recebidas, peer_ip, peer_port, peer_socket):
    # DEVE RECEBER O JOIN E A LISTA, E USAR UM SPLIT POR EXEMPLO PARA SEPARAR NA STRING
    print("### OPERACAO JOIN ###")
    # RECEBER E SALVAR LISTA DE ARQUIVOS NO SERVIDOR
    key_dic = "" + peer_ip + ":" + str(peer_port)
    lista_arquivos_recebida = informacoes_recebidas
    salvarListaArquivos(key_dic, lista_arquivos_recebida)
    peer_socket.send("JOIN_OK".encode())

def operacaoSearch(nome_arquivo, peer_socket):
    ## Mandar lista para peer printar
    lista_peers_contem_arquivo_buscado = str(buscarArquivo(nome_arquivo))
    peer_socket.send(lista_peers_contem_arquivo_buscado.encode())


# Definindo a thread para que seja possivel mais de uma conexao ao servidor
class HandlePeerThread(threading.Thread):
    def __init__(self, peerAddress, peerSocket):
        threading.Thread.__init__(self)
        self.peerSocket = peerSocket
        self.peerAddress = peerAddress
        print("New connection added: ", peerAddress)

    def run(self):
        mensagem_recebida = ''
        while True:
            # Recebendo e tratando mensagem do peer
            data = self.peerSocket.recv(2048)
            mensagem_recebida = data.decode()
            peer_ip, peer_port = self.peerAddress
            if mensagem_recebida == 'quit':
                print("Mensagem recebida: " + mensagem_recebida)
                break
            mensagem_ajustada, operacao, informacoes_recebidas = ajustarMensagemRecebida(mensagem_recebida)
            if operacao == "JOIN":
                operacaoJoin(informacoes_recebidas, peer_ip, peer_port, self.peerSocket)

            if operacao == "SEARCH":
                print("### OPERACAO SEARCH ###")
                nome_arquivo = informacoes_recebidas
                operacaoSearch(nome_arquivo, self.peerSocket)


            if operacao == "DOWNLOAD":
                print("### OPERACAO DOWNLOAD ###")
                nome_arquivo_download = informacoes_recebidas
                lista_peers_contem_arquivo_buscado_para_download = str(buscarArquivo(nome_arquivo_download))
                self.peerSocket.send(lista_peers_contem_arquivo_buscado_para_download.encode())

        print("Peer at ", self.peerAddress, " disconnected...")



def main():
    serverSocket = configurarServidor()
    try:
        abrirConexaoServidor(serverSocket)
        listening(serverSocket)
    finally:
        fecharConexaoServidor(serverSocket)

if __name__ == '__main__':
    main()










