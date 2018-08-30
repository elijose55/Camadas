#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading

# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """
    
    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        size = 0   

        while(self.getBufferLen() > size):
            time.sleep(2)
            print("esperando")
            size = self.getBufferLen()

        if size == 0:
            return (0,0)
        else:
            return(self.getBuffer(size),size)


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
    
    def desfaz_package(self, package):
        #Faz o desempacotamento dos dados baseado-se no protocolo GG7.
        #Separa o payload do restante e verifica se o tamanho do payload esta correto
        head_size = 4
        found_eop = False
        erro = 0
        byte_stuff = bytes.fromhex("AA")
        eop = bytes.fromhex("FF FE FD FC")
        head = package[0:4]
        print(head)
        package = package[4:]
        payload_size = int.from_bytes(head, byteorder = "big")
        for i in range(len(package)):
            if package[i:i+4] == eop:
                if package[i-1] == byte_stuff:
                    #retira os bytes stuff
                    p1 = package[0:i-1]
                    p2 = package[i:]
                    package = p1 + p2
                else:
                    found_eop = True
                    print("EOP encontrado na posição:{0}".format(i))
                    package = package[0:-4]
                    if len(package) != payload_size:
                        print("ERRO! Número de Bytes do Payload diferentes do informado no HEAD. Bytes Payload recebido:{0}".format(len(package)))
                        print("Bytes que foram enviados:{0}".format(payload_size))
                        erro = 1
                    return erro
        if not found_eop:
            print("ERRO! EOP não encontrado")
            erro = 1
            return erro
        payload = package
        print(len(payload))
        return payload
                



