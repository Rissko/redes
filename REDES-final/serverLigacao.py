import threading
from socket import *
from tkinter import INSERT, END

import pyaudio


def finalizaConexao(busy):
    try:
        if busy.flag['online']:
            servidorUdp.sendto("encerrar_ligacao".encode(), origem_call)
            busy.flag['online'] = False
    except:
        pass


def iniciarServidorLigacao(meuIp, callback, endcallbtn, busy, console, connectbtn):
    global servidorUdp
    global origem_call
    global output_stream
    busy.flag['online'] = False
    HOST = meuIp
    PORT = 6301
    servidorUdp = socket(AF_INET, SOCK_DGRAM)
    origem = (HOST, PORT)
    servidorUdp.bind(origem)
    write(console, "Iniciando servidor de ligação")
    py_audio = pyaudio.PyAudio()
    buffer = 4096  # 127.0.0.1
    output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
    while True:
        msg, origem_call = servidorUdp.recvfrom(4096)
        if "convite" in str(msg):
            if busy.flag['online']:
                servidorUdp.sendto("resposta_ao_convite/ocupado".encode(), origem_call)
            else:
                split = str(msg).split('/')
                resp = callback(origem_call, split[1])
                if "s" in resp:
                    write(console, "Convite Aceito")
                    write(console, "Começando ligação...")
                    output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=44100, channels=2, frames_per_buffer=buffer)
                    servidorUdp.sendto("resposta_ao_convite/aceito".encode(), origem_call)
                    busy.flag['online'] = True
                    endcallbtn['state'] = "active"
                    connectbtn['state'] = "disabled"
                    thread2 = threading.Thread(target=enviarAudio, args=(busy,endcallbtn,console, connectbtn))
                    thread2.start()
                elif "n" in resp:
                    servidorUdp.sendto("resposta_ao_convite/rejeitado".encode(), origem_call)
        elif "encerrar_ligacao" in str(msg):
            busy.flag['online'] = False
            endcallbtn['state'] = "disabled"
            connectbtn['state'] = "active"
        if busy.flag['online']:
            output_stream.write(msg)


def enviarAudio(busy,endcallbtn,console,connectbtn):
    global py_audio
    global input_stream
    py_audio = pyaudio.PyAudio()
    buffer = 1024
    input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44100, channels=2, frames_per_buffer=buffer)
    while busy.flag['online']:
        data = input_stream.read(buffer)
        servidorUdp.sendto(data, origem_call)
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
