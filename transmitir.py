
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação - Transmissor
####################################################

print("comecou")

from enlace import *
import time
from PIL import Image
from array import array
import tkinter as tk
from tkinter.filedialog import askopenfilename
import time

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)
baudrate    = 115200

print("porta COM aberta com sucesso")

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        
        self.selectbutton = tk.Button(self, text="Selecionar imagem", fg="black",
                              command=self.selectimage)

        self.selectbutton.pack(side="top")              

        self.sendbutton = tk.Button(self, text="Enviar imagem", fg="black",
                              command=self.sendimage)
        self.sendbutton.pack(side="top")

        self.quit = tk.Button(self, text="Fechar janela", fg="black",
                              command=root.destroy)
        self.quit.pack(side="bottom")

    def selectimage(self):
        self.filename = askopenfilename() 
        print("Imagem selecionada")   
        
    def sendimage(self):
        root.destroy()
        print("Mensagem enviada")


def tempo_teorico(n_bytes,baudrate):
    t = (n_bytes*10)/baudrate
    return t

def main(imagem):
    
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")


    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("gerando dados para transmissao :")

    with open(imagem, "rb") as imageFile:
        f = imageFile.read()
        img = bytearray(f)
    txBuffer = bytes(img)
    print(txBuffer)
    txLen    = len(txBuffer)

    # ListTxBuffer = list()
    # for x in range(0,20):
    #     ListTxBuffer.append(x)
    # txBuffer = bytes(ListTxBuffer)
    # txLen    = len(txBuffer)
    # print(txLen)

    # Transmite dado
    print(" Tamanho da imagem: {0} bytes".format(txLen))
    print("tentado transmitir .... {0} bytes".format(txLen))
    starttime = time.time()

    len_Payload = com.sendData(txBuffer)


        
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
   

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    finaltime = time.time() - starttime
    print("Tempo esperado da transmissão : {0} bytes".format(tempo_teorico(txLen,baudrate)))
    print("Tempo da transmissão : {0} segundos".format(finaltime))
    print("Throughput:{0}".format(len_Payload/finaltime))
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    main(app.filename)
