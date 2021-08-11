from tkinter import *
from socket import *
import threading


def receive():
    global client
    client = socket(AF_INET, SOCK_STREAM)
    ip_info = ip.get()
    HOST = ip_info
    PORT = 5000
    client.connect((HOST, PORT))
    client.send(name.get().encode('ascii'))
    message = client.recv(1024).decode('ascii')
    if message == "Ja existe um usuario com o mesmo nome":
        print(message)
    elif message == "Conectado ao servidor / end":
        split = message.split("/")
        print(split[0])
        registrybtn['state'] = "disabled"
        registryentry['state'] = "disabled"
        connectbtn['state'] = "active"
        connectentry['state'] = "normal"
        endbtn['state'] = "active"
        atualizarbtn['state']="active"
        ipentry['state']="disabled"
        thread = threading.Thread(target=listen)
        thread.start()

def listen():
    while True:
        message = client.recv(1024).decode('ascii')
        if message == "atualiza":
            message = client.recv(1024).decode('ascii')
            print(message)
        elif message == "Nao e possivel conectar a si mesmo":
            print(message)
        elif message == "Nome nao encontrado":
            print(message)
        elif "finish" in message:
            print(message)
            print("Conexão encerrada")
            screen.destroy()
        elif "socket" in message:
            message = client.recv(1024).decode('ascii')
            print(f"Conectado ao usuário {message}")
            connectbtn['state'] = "disabled"
            connectentry['state'] = "disabled"
        elif "repeat" in message:
            message = client.recv(1024).decode('ascii')
            print(message)

def sendName():
    dest_info = dest.get()
    client.send("nameRequest".encode('ascii'))
    client.send(dest_info.encode('ascii'))


def closeConn():#Jv
    client.send("closeConn".encode('ascii'))

def atualiza():
    client.send("atualiza".encode('ascii'))

def closeConnThread():
    thread = threading.Thread(target=closeConn)
    thread.start()


def sendNameThread():
    thread = threading.Thread(target=sendName)
    thread.start()

def receiveThread():
    thread = threading.Thread(target=receive)
    thread.start()

def main():
    global name
    global dest
    global ip
    global screen
    global registryentry
    global registrybtn
    global connectentry
    global connectbtn
    global endbtn
    global atualizarbtn
    global ipentry
    screen = Tk()
    screen.geometry("300x420")
    screen.title("Sala Virtual")
    name = StringVar()
    dest = StringVar()
    ip = StringVar()
    Label(text="").pack()
    atualizarbtn = Button(text="Mostrar usuarios conectados", height="2", width="30",state="disabled", command=atualiza)
    atualizarbtn.pack()
    Label(text="").pack()
    connectbtn = Button(text="Procurar usuário e conectar", height="2", width="30",state="disabled", command=sendNameThread)
    connectbtn.pack()
    Label(text="").pack()
    connectentry = Entry(textvariable=dest,state="disabled")
    connectentry.pack()
    Label(text="").pack()
    registrybtn = Button(text="Registro", height="2", width="30", command=receiveThread)
    Label(text="").pack()
    registrybtn.pack()
    Label(text="").pack()
    Label(text="Nome*:").pack()
    registryentry = Entry(textvariable=name)
    registryentry.pack()
    Label(text="IP*:").pack()
    ipentry = Entry(textvariable=ip)
    ipentry.pack()
    Label(text="").pack()
    endbtn = Button(text="Encerrar Conexão", height="2", width="30", state="disabled", command=closeConnThread)
    endbtn.pack()
    screen.mainloop()

main()
