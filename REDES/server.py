from socket import *
import threading
import time

HOST = "127.0.0.1"
PORT = 5000

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Aguardando conexão de um cliente")
clients = []
names = []
connections = []

def broadcast(message):
    for client in clients:
        client.send("broadcast".encode('ascii'))# Não precisa enviar pra quem acabou de entrar na sala. Só pra quem já estava.
        client.send(message)


def handle(client):
    while True:
        estado = client.recv(1024).decode('ascii')
        if estado == "atualiza":
            client.send("atualiza".encode('ascii'))
            peers = ''
            for i in clients:
                index = clients.index(i)
                peers += str(i.getpeername())
            client.send((str(names) + "/" + (peers)).encode('ascii'))
        elif estado == "closeConn":
            for i in clients:
                if i == client:
                    index = clients.index(client)
            for ind,tuple in enumerate(connections):
                t1 = tuple[0]
                t2 = tuple[1]
                if t1 == names[index] or t2 == names[index]:
                    del connections[ind]
            names.remove(names[index])
            client.send("finish".encode('ascii'))
            client.close()
            clients.remove(client)
            print(connections)
            showConnections()
            break
        elif estado == "nameRequest":
            requestedName = client.recv(1024).decode('ascii')
            if requestedName == names[clients.index(client)]:
                client.send("Nao e possivel conectar a si mesmo".encode('ascii'))
            elif requestedName not in names:
                client.send("Nome nao encontrado".encode('ascii'))
            else:
                i = names.index(requestedName)
                if connections == []:
                    client.send("socket".encode('ascii'))
                    index = clients.index(client)
                    connections.append((names[index], requestedName))
                    client.send((names[i] + str(clients[i].getpeername())).encode('ascii'))
                    clients[i].send("socket".encode('ascii'))
                    clients[i].send((names[index] + str(clients[index].getpeername())).encode('ascii'))
                else:
                    for pos, tuple in enumerate(connections):
                        t1 = tuple[0]
                        t2 = tuple[1]
                        index = clients.index(client)
                        if t1 != names[i] and t2 != names[i]:
                            client.send("socket".encode('ascii'))
                            connections.append((names[index], requestedName))
                            client.send((names[i] + str(clients[i].getpeername())).encode('ascii'))
                            clients[i].send("socket".encode('ascii'))
                            clients[i].send((names[index] + str(clients[index].getpeername())).encode('ascii'))
                        elif t1 == names[i] or t2 == names[i]:
                            client.send("repeat".encode('ascii'))
                            client.send("Esse usuario ja esta conectado a alguem".encode('ascii'))




def receive():
    while True:
        client, address = s.accept()
        name = client.recv(1024).decode('ascii')
        if name in names:
            client.send("Ja existe um usuario com o mesmo nome".encode('ascii'))
        if name not in names:
            print("Conectado em", str(address))
            names.append(name)
            clients.append(client)
            print(f"Nome do cliente é: {name}")
            client.send("Conectado ao servidor / end".encode('ascii'))
            showConnections()
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()


def showConnections():
    print("REGISTRO DE USUÁRIOS: \n")
    if clients == []:
        print("VAZIO")
    else:
        for client in clients:
            print(names[clients.index(client)] + str(client.getpeername()))


receive()
