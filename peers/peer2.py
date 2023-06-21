import socket
## Definindo server a ser conectado
SERVER = "127.0.0.1"
PORT = 8080
## Criando/configurando o socket do peer
peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## Conectando com o servidor
peerSocket.connect((SERVER, PORT))
## Mandando mensagem do peer para o servidor
peerSocket.sendall(bytes("This is from Client",'UTF-8'))

## loop para ficar escutando o servidor
while True:
    ## Recebe mensagem do servidor
    in_data = peerSocket.recv(1024)
    print("From Server :", in_data.decode())
    ## input para entrada ate receber o 'bye'
    out_data = input()
    ## envia mensagem do teclado para o servidor
    peerSocket.sendall(bytes(out_data,'UTF-8'))
    if out_data == 'quit':
        break

peerSocket.close()

