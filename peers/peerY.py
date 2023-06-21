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

operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")

def listPeerFiles():
    diretorio = "directoryY"
    list_files = os.listdir(diretorio)
    return list_files

    ## JOIN OPERATION
if operacao == '1':
    # diretorio0 = input("Defina um diretorio para o peer: ")
    lista_arquivos = listPeerFiles()

    # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
    mensagem_join = []
    mensagem_join.append("JOIN")
    mensagem_join.append(lista_arquivos)
    print(mensagem_join)
    ## MANDAR A OPERACAO JOIN E A LISTA PARA O SERVIDOR
    s.send(str(mensagem_join).encode())
    print("ENVIADO MENSAGEM JOIN COM LISTA")
    if s.recv(1024).decode() == "JOIN_OK":
        print("Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + ", ".join(lista_arquivos))

## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
elif operacao == '2':
    arquivo = input("Arquivo a ser buscado: ")
    ## Manda operacao e qual o arquivo o servidor deve buscar
    mensagem_search = []
    mensagem_search.append("SEARCH")
    mensagem_search.append(arquivo)
    print(mensagem_search)
    print(type(mensagem_search))
    s.send(str(mensagem_search).encode())
    print("MANDOU OP E ARQUIVO A SER BUSCADO NO SERVIDOR")
    peers_list = s.recv(1024).decode()
    print("peers com arquivo solicitado: " + peers_list) ## talvez precise do IP e porta do peer
    print("SEARCH Finalizado")


# close connection
s.close()
