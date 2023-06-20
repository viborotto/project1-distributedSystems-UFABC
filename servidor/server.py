import socket

s = socket.socket()
print("Server Socket EP1 created")

port = 1099

s.bind(('', port))
print("server socket binded to %s" %(port))

# put socket into listening mode
s.listen(5)
print("server socket is listening")

def receberMensagem(c):
    return c.recv(1024).decode()


## realizar busca na estrutura de dados e retornar lista vazia ou de peers
def buscarArquivo(nomeArquivo):
    print("INICIANDO BUSCA DE ARQUIVO NO DICIONARIO")
    listaPeers = []
    return listaPeers

# a forever loop until or interrupt it or an error occurs
while True:
    # Estabilish connection with client
    c, addr = s.accept()

    # send JOIN_OK message to peer
    if receberMensagem(c) == "JOIN":
        print("SERVIDOR RECEBEU O JOIN")
        c.send("JOIN_OK".encode())
        print("JOIN_OK DO SERVIDOR ENVIADO")
        # RECEBER E SALVAR LISTA DE ARQUIVOS NO SERVIDOR
        files_list_received = receberMensagem(c)
        print(files_list_received)
        print("JOIN Finalizado")

    if receberMensagem(c) == "SEARCH":
        print("SERVIDOR RECEBEU O SEARCH")
        nome_arquivo = receberMensagem(c)
        print("NOME DO ARQUIVO RECEBIDO NO SERVIDOR: " + nome_arquivo)
        ## Mandar lista para peer printar
        c.send(str(buscarArquivo(nome_arquivo)).encode())
        print("BUSCOU E ENVIOU LISTA DE PEERS QUE CONTEM O ARQUIVO")



