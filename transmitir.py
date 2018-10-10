
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
from tkinter import Tk
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
serialName = "COM6"                  # Windows(variacao de)
baudrate    = 115200

print("porta COM aberta com sucesso")


def tempo_teorico(n_bytes,baudrate):
    t = (n_bytes*10)/baudrate
    return t

def main():
    
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


    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    txBuffer = open(filename, "rb").read()
    txLen = len(txBuffer)
    print("Tamanho do dado: {0} bytes".format(txLen))
    print('----------------------------')

    com.comunicacao(txBuffer,"client")


    # Transmite dado
    



    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()


    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    #finaltime = time.time() - starttime
    #print("Tempo esperado da transmissão : {0} bytes".format(tempo_teorico(txLen,baudrate)))
    #print("Tempo da transmissão : {0} segundos".format(finaltime))
    #print("Throughput:{0}".format(len_Payload/finaltime))
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
