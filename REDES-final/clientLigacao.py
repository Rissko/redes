import socket
import threading
from tkinter import INSERT, END

import pyaudio
import time


def iniciaConexaoUDP(dest_ip, origem_name, endcallbtn, busy, console, connectbtn):
    global conexaoUdp
    global dest
    write(console," Destino: " + str(dest_ip))
    HOST = dest_ip
    PORT = 6000
    conexaoUdp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    dest = (HOST, PORT)
    write(console,"Enviando convite")
    conexaoUdp.sendto(("convite/" + origem_name).encode(), dest)
    thread = threading.Thread(target=ouvirResposta, args=(conexaoUdp, endcallbtn, busy, console, connectbtn))
    thread.start()


def finalizaConexao(busy):
    try:
        if busy.flag['online']:
            conexaoUdp.sendto("encerrar_ligacao".encode(), dest)
            busy.flag['online'] = False
    except:
        pass


def ouvirResposta(conexaoUdp, endcallbtn, busy, console, connectbtn):
    global output_stream
    global py_audio
    py_audio = pyaudio.PyAudio()
    buffer = 4096
    output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2,
                                  frames_per_buffer=buffer)
    while True:
        msg, endereco = conexaoUdp.recvfrom(4096)
        if "aceito" in str(msg):
            write(console,"Iniciando chamada")
            busy.flag['online'] = True
            endcallbtn['state'] = "active"
            connectbtn['state'] = "disabled"
            thread = threading.Thread(target=send_audio, args=(endereco, busy, console,endcallbtn, connectbtn))
            thread.start()
        elif "rejeitado" in str(msg):
            write(console,"Convite rejeitado")
        elif "ocupado" in str(msg):
            write(console,"Usuário está ocupado")
        elif "encerrar_ligacao" in str(msg):
            busy.flag['online'] = False
            endcallbtn['state'] = "disabled"
            connectbtn['state'] = "active"
        elif busy.flag['online']:
            output_stream.write(msg)


def send_audio(dest, busy, console,endcallbtn, connectbtn):
    global input_stream
    global py_audio
    write(console, "Destino: " + str(dest))
    buffer = 1024

    input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2, frames_per_buffer=buffer)

    while busy.flag['online']:
        data = input_stream.read(buffer)
        conexaoUdp.sendto(data, dest)
    busy.flag['online'] = False
    endcallbtn['state'] = "disabled"
    connectbtn['state'] = "active"
    write(console, "Ligacao finalizada")
    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    py_audio.terminate()

def write(console, *message, end = "\n", sep = " "):
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    console.insert(INSERT, text)
    console.see(END)