import socket
import ast

s = socket.socket()
print("Server Socket EP1 created")

port = 1099
s.bind(('', port))
print("server socket binded to %s" %(port))

# put socket into listening mode
s.listen(5)
print("server socket is listening")

dicionarioPeers = {}

def receberMensagem(c):
    return c.recv(1024).decode()

def ajustarMensagemRecebida(mensagem_recebida):
    print("ajustar mensagem recebida")
    print(mensagem_recebida)
    ajustada = ast.literal_eval(mensagem_recebida)
    print(ajustada)
    return ajustada

def salvarListaArquivos(key_dic, lista_arquivos_recebida):
    print("salvar lista de arquivos")
    ## OBJETIVO
    #dicionarioPeers = {"ip:port": ["arquivo1.txt", "arquivo2.txt"]}
    dicionarioPeers[key_dic] = lista_arquivos_recebida
    print(dicionarioPeers)

    ## realizar busca na estrutura de dados e retornar lista vazia ou de peers
def buscarArquivo(nomeArquivo):
    print("INICIANDO BUSCA DE ARQUIVO NO DICIONARIO:")
    print(dicionarioPeers)
    listaPeers = []
    return listaPeers


    # a forever loop until or interrupt it or an error occurs
while True:
    # Estabilish connection with client
    c, addr = s.accept()
    peer_ip, peer_port = addr

    mensagem_recebida = receberMensagem(c)
    print(mensagem_recebida)
    mensagem_ajustada = ajustarMensagemRecebida(mensagem_recebida)
    print(mensagem_ajustada)
    operacao = mensagem_ajustada[0]
    print(operacao)
    print(type(operacao))
    informacoes_recebidas = mensagem_ajustada[1]
    print(informacoes_recebidas)
    print(type(informacoes_recebidas))

    if operacao == "JOIN":
        #DEVE RECEBER O JOIN E A LISTA, E USAR UM SPLIT POR EXEMPLO PARA SEPARAR NA STRING
        print("SERVIDOR RECEBEU O JOIN")
        # RECEBER E SALVAR LISTA DE ARQUIVOS NO SERVIDOR
        key_dic = "" + peer_ip + ":" + str(peer_port)
        lista_arquivos_recebida = informacoes_recebidas
        salvarListaArquivos(key_dic, lista_arquivos_recebida)
        c.send("JOIN_OK".encode())
        print("JOIN_OK DO SERVIDOR ENVIADO")
        

    if operacao == "SEARCH":
        print("SERVIDOR RECEBEU O SEARCH")
        nome_arquivo = informacoes_recebidas
        print("NOME DO ARQUIVO RECEBIDO NO SERVIDOR: " + nome_arquivo)
        ## Mandar lista para peer printar
        c.send(str(buscarArquivo(nome_arquivo)).encode())
        print("BUSCOU E ENVIOU LISTA DE PEERS QUE CONTEM O ARQUIVO")



