##Interface Fisica
## Eli Jose e Nicolas Barbosa

from enlace import *
from graphic import findimg
import time
from identify import *
from tkinter import *
from PIL import Image

serialName = "COM3"


def main():

    # Inicializa enlace 
    com = enlace(serialName)
    print("porta COM3 aberta com sucesso")

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação com transmissor aberta")

    print ("gerando dados para transmissao :")

#--------------------------------------------------------------#
    byte_nulo = bytes(10)
    com.sendData(1,byte_nulo)
    print("Mensagem tipo 1 enviada")
    time.sleep(2)

    tipo_recebido, head2, payload2 = listen_and_tell(com,1,byte_nulo,2)
    com.sendData(3,byte_nulo)

    #bnone = bytes(10)
    #com.sendData(1,bnone)
    #print("----Tipo 1 enviada, aguardando 2----")
    #time.sleep(2)
    #two , head2 , payload2 = listen_and_tell(com,1,bnone,2)
    #com.sendData(3,bnone)

    #---------------------------------------------------------#



    #---------------------------------------------------------#

    print ("gerando dados para transmissao - etapa 2:")

    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

    txBuffer = open(filename, "rb").read()
    txLen = len(txBuffer)

    # Transmite dado
    tempo_teorico = (txLen*10)/baudrate
    print(" Tamanho da imagem: {0} bytes".format(txLen))
    print("tentado transmitir .... {0} bytes".format(txLen))
    print("-------------------------")
    print("Tempo esperado da transmissão : {0} bytes".format(tempo_teorico))
    print("-------------------------")
    starttime = time.time()

    com.sendData(4,txBuffer)

    finaltime = time.time() - starttime
    print("-------------------------")
    print("Tempo da transmissão : {0} segundos".format(finaltime))

    print("- Mensagem tipo 4 enviada, aguardando 5 ou 6 -")

    tipo_recebido, head56, payload56 = listen_and_tell_double(com,4,txBuffer,5,6)


    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()

    #---------------------------------------------------------#

    com.sendData(7,byte_nulo)
    print("Encerrando transmissão") 
    com.disable()

if __name__ == "__main__":
    main()
