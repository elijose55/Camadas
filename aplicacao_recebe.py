#Camada Fisica
#Eli Jose e Nicolas Barbosa

from enlace import *
import time
from identify import *
from PIL import Image

serialName = "COM3"
baudrate    = 115200


def tempo_teorico(n_bytes,baudrate):
    t = (n_bytes*10)/baudrate
    return t

def main():

    # Inicializa enlace 
    com = enlace(serialName)
    print("porta COM3 aberta com sucesso") 
    # Ativa comunicacao
    
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação com recebedor aberta")


    #---------------------------------------------------------#

    byte_nulo = bytes(10)
    tipo_recebido, head, payload = only_listen(com,1)
    com.sendData(2,byte_nulo)

    print("- Mensagem tipo 2 enviada, aguardando 3 -")
    tipo_recebido, head, payload  = listen_and_tell(com,2,bnone,3)

    #---------------------------------------------------------#
    #four , head4 , payload4 , payloadsize4 = only_listen(com,4)
    ##consistência

    tipo_recebido, head4, payload , payloadsize4 = only_listen(com,4)

    #Controle de qualidade:
    if int.from_bytes(head4[-2:],byteorder = "big") != payloadsize4:
        com.sendData(6,byte_nulo)
        print("- Mensagem tipo 6 enviada -")
        tipo_recebido, head4, payload , payloadsize4 = only_listen(com,4)

    else:
        com.sendData(5,byte_nulo)
        print("- Mensagem tipo 5 enviada -")



    #previsão de tempo de transmissão
    tempo_teorico = (payloadsize4*10)/baudrate
    bdr = com.tx.fisica.baudrate
    print("-------------------------")
    print("Tempo esperado da transmissão : {0} bytes".format(tempo_teorico)
    print("-------------------------")

    # log
    print ("Lido              {} bytes ".format(payloadsize4))
    

    # Salva a Imagem
    x = open('NovaImg.png','wb')
    x.write(rxBuffer)
    x.close()


    # Encerra comunicação
    print("-------------------------")
    print("Imagem salva")
    print("-------------------------")

    tipo_recebido, head4, payload , payloadsize4 = only_listen(com,7)
    print("Encerramento foi solicitado e aceito")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
