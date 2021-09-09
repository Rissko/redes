import time
from socket import *
import threading

HOST = "25.5.67.88"
PORT = 5000

s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
print("Aguardando conexão de um cliente")
clients = []
names = []
connections = []

def broadcast(message):
    time.sleep(0.5)
    for client in clients:
        client.send(("broadcast" "/" + message).encode())

def receive():
    while True:
        client, address = s.accept()
        name = client.recv(1024).decode()
        if name in names:
            client.send("Ja existe um usuario com o mesmo nome".encode())
        if name not in names:
            print("Conectado em", str(address))
            names.append(name)
            clients.append(client)
            print(f"Nome do cliente é: {name}")
            client.send(("Conectado ao servidor /" + address[0]).encode())
            showConnections()
            stringNames = ''
            for i in names:
                stringNames += i + "\n"
            broadcast(stringNames)
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()

def handle(client):
    global requested_name
    while True:
        estado = client.recv(1024).decode()
        if estado == "atualiza":
            client.send("atualiza".encode())
            peers = ''
            for i in clients:
                peers += str(i.getpeername())
            client.send((str(names) + "/" + (peers)).encode())
        elif estado == "closeConn":
            index = clients.index(client)
            for ind,tuple in enumerate(connections):
                t1 = tuple[0]
                t2 = tuple[1]
                if t1 == names[index] or t2 == names[index]:
                    del connections[ind]
            names.remove(names[index])
            stringNames = ''
            for i in names:
                stringNames += i + "\n"
            broadcast(stringNames)
            client.send("finish".encode())
            client.close()
            clients.remove(client)
            print(connections)
            showConnections()
            break
        elif estado == "consulta":
            requested_name = client.recv(1024).decode()
            if requested_name == names[clients.index(client)]:
                client.send("Nao e possivel conectar a si mesmo".encode())
            elif requested_name not in names:
                client.send("Nome nao encontrado".encode())
            else:
                i = names.index(requested_name)
                host, port = clients[i].getpeername()
                client.send(("endereco/" + str(host) + "/" + str(port) + "/" + names[clients.index(client)]).encode())

def showConnections():
    print("REGISTRO DE USUÁRIOS: \n")
    if clients == []:
        print("VAZIO")
    else:
        for client in clients:
            print(names[clients.index(client)] + str(client.getpeername()))


receive()
