import socket, os

s = socket.socket()
file_name = "arquivo.mp4"

# define the port on which you want connect
# nesse caso a porta que definimos no servidor
server_port = 1099
server_ip = '127.0.0.1'

s.connect((server_ip, server_port))
peer_ip, peer_port = s.getsockname()

operacao = input("Operacao voce deseja realizar (1. JOIN, 2. SEARCH, 3. DOWNLOAD): ")

def listPeerFiles():
    list_files = os.listdir(diretorio)
    return list_files


    ## JOIN OPERATION
if operacao == '1':

    s.send("JOIN".encode())
    print("peer mandou JOIN para o servidor")
    if s.recv(1024).decode() == "JOIN_OK":
        diretorio = input("Defina um diretorio para o peer: ")
        print("Sou peer " + peer_ip + ":" + str(peer_port) + " com arquivos " + str(listPeerFiles()))
        # Enviar lista de arquivos para servidor salvar em uma estrutura de dados
        s.send(str(listPeerFiles()).encode())

## SEARCH OPERATION: busca no servidor em quais peers o arquivo esta disponivel
elif operacao == '2':
    s.send("SEARCH".encode())
    print("peer mandou SEARCH para o servidor")
    arquivo = input("Arquivo a ser buscado: ")
    ## Manda informacao de qual o arquivo o servidor deve buscar
    s.send(arquivo.encode())
    print("MANDOU ARQUIVO A SER BUSCADO NO SERVIDOR")
    peers_list = s.recv(1024).decode()
    print("peers com arquivo solicitado: " + peers_list) ## talvez precise do IP e porta do peer
    print("SEARCH Finalizado")


# close connection
s.close()
