import socket, threading
import ast

# Estrutura de dados para armazenamento de informacoes Peers - Dicionario
# Key: "ipPeer:portaPeer"
# Value: lista de arquivos e.g: ["arquivo1.mp4", "arquivo2.mp4"]
dicionario_peers = {}

# Atribuir uma porta e ip ao servidor, para que crie o socket e vincule o socket com o ip e porta definidos
def configurarServidor():
    server_port = 1099
    server_ip = "127.0.0.1"
    # Inicializando/Configurando Server Socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    return server_socket

def servidorModoListening(server_socket):
    # Loop para ficar escutando a forever loop until or interrupt it or an error occurs
    # put socket into listening mode
    server_socket.listen(5)
    print("server socket is listening")


def fecharConexaoServidor(server_socket):
    server_socket.close()

# Funcao para aceitar a conexao
def conectarComPeer(server_socket):
    # Loop pois vamos aguardar a cada peer se conectar ao servidor
    while True:
        # Aceita e estabelece conexao com um peer disponivel
        peer_socket, peer_address = server_socket.accept()
        print("Server Connection accepted")
        print("###########################")
        # Separando as informacoes em duas variaveis peer_ip e peer_port
        peer_ip, peer_port = peer_address
        # inicializa uma thread de peer para um processo a parte
        new_peer_thread = HandlePeerThread(peer_address, peer_socket)
        new_peer_thread.start()


# Funcao para tratar a string recebida do peer, separando em uma lista com operacao e arquivos do peer
def ajustarMensagemRecebida(mensagem_recebida):
    ajustada = ast.literal_eval(mensagem_recebida)
    print("ajustada: " + str(ajustada))
    operacao = ajustada[0]
    informacoes_recebidas = ajustada[1]
    print("informacoes_recebidas: " + str(ajustada[1]))
    return ajustada, operacao, informacoes_recebidas


# Funcao para salvar as informacoes recebidas do peer em um dicionario
def salvarListaArquivos(key_dic, lista_arquivos_recebida):
    #dicionarioPeers = {"ip:port": ["arquivo1.txt", "arquivo2.txt"]}
    dicionario_peers[key_dic] = lista_arquivos_recebida
    print("Peer " + key_dic + " adicionado com arquivos " + ", ".join(dicionario_peers[key_dic]))
    print(dicionario_peers)


# Funcao para realizar busca na estrutura de dados e retornar lista vazia ou de peers
def buscarArquivo(nome_arquivo):
    listaPeers = []
    for key_dic, value in dicionario_peers.items():
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
    print("### OPERACAO SEARCH ###")
    ## Mandar lista para peer printar
    lista_peers_contem_arquivo_buscado = str(buscarArquivo(nome_arquivo))
    peer_socket.send(lista_peers_contem_arquivo_buscado.encode())


# Definindo a thread para que seja possivel mais de uma conexao ao servidor
class HandlePeerThread(threading.Thread):
    def __init__(self, peer_address, peer_socket):
        threading.Thread.__init__(self)
        self.peer_socket = peer_socket
        self.peer_address = peer_address
        print("New connection added: ", peer_address)

    def run(self):
            mensagem_recebida = ''
        # while True:
            # Recebendo e tratando mensagem do peer
            data = self.peer_socket.recv(1024)
            print("data apos receive: " + str(data))
            mensagem_recebida = data.decode()

            if mensagem_recebida == '':
                print("MENSAGEM VAZIA")


            # Obtendo o peer_ip e o peer_port do Peer conectado ao servidor
            peer_ip, peer_port = self.peer_address

            # Ajusta a mensagem caso nao seja vazia
            if mensagem_recebida != '':
                mensagem_ajustada, operacao, informacoes_recebidas = ajustarMensagemRecebida(mensagem_recebida)

                if operacao == "JOIN":
                    operacaoJoin(informacoes_recebidas, peer_ip, peer_port, self.peer_socket)

                if operacao == "SEARCH":
                    nome_arquivo = informacoes_recebidas
                    operacaoSearch(nome_arquivo, self.peer_socket)
                    print("Peer " + str(peer_ip) + ":" + str(peer_port) + " solicitou arquivo " + nome_arquivo)

                if operacao == "DOWNLOAD":
                    nome_arquivo_download = informacoes_recebidas
                    lista_peers_contem_arquivo_buscado_para_download = str(buscarArquivo(nome_arquivo_download))
                    self.peer_socket.send(lista_peers_contem_arquivo_buscado_para_download.encode())

                if mensagem_recebida == 'quit':
                    print("Mensagem recebida: " + mensagem_recebida)

            ## ao finalizar a operacao, fecha a conexao com o peer [?]
            self.peer_socket.close()
            print("Peer at ", self.peer_address, " disconnected...")



def main():
    # Configura ip, porta, criar o serverSocket e faz o bind
    server_socket = configurarServidor()
    try:
        servidorModoListening(server_socket)
        conectarComPeer(server_socket)
    finally:
        # para de escutar e encerra
        fecharConexaoServidor(server_socket)

if __name__ == '__main__':
    main()










