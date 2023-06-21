import socket, threading
class PeerThread(threading.Thread):
    def __init__(self,peerAddress,peerSocket):
        threading.Thread.__init__(self)
        self.csocket = peerSocket
        print("New connection added: ", peerAddress)

    def run(self):
        print("Connection from : ", peerAddress)
        msg = ''
        while True:
            # recebendo mensagem do peer
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == 'bye':
                break
            print("from client", msg)
            self.csocket.send(bytes(msg, 'UTF-8'))
        print("Peer at ", peerAddress, " disconnected...")


## Inicializando server
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for peer request..")

while True:
    server.listen(1)
    peerSocket, peerAddress = server.accept()
    print("Server Connection accepeted")
    # inicializa uma thread de peer
    newthread = PeerThread(peerAddress, peerSocket)
    newthread.start()

