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
        self.head        = 10

    def thread(self): 
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        #TIMERRRRRRRRRRRRRRRRRRR (como estimar?)
        while not self.threadStop:
            start_time = time.time()
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

    def getNData(self, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
        head_size = 10
        tamanho = self.getBufferLen()
        
        #esperando pegar todos os dados no buffer
        if self.getBufferLen() < size:
            print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,tamanho))
        while(self.getBufferLen() < size):
             time.sleep(0.05)

        
        package = self.getBuffer(size)
        head = package[:head_size]
        payload = package[head_size:]

        #byte_stuff = bytes.fromhex("AA")
        #eop = bytes.fromhex("FF FE FD FC")
        byte_stuff = bytes('A','utf-8')
        eop = bytes('abcdef','utf-8')


        encontrou = False

        for i in range(len(payload)-5):
            if payload[i:i+6] == eop:
                if payload[i-1] == byte_stuff[0]:
                    payload = payload[:i-1] + payload[i+6:] 
                    
                    print("Stuffing e EOP retirados")
                    
                else:
                    encontrou = True
                    print("============== END OF PACKAGE in byte {} =============".format(i+11))
                    
        if not encontrou :
            print("ERRO!!! EOP NÃO ENCONTRADO")

        payload2 = payload[:-6]

        headlen = int.from_bytes(head[-2:], byteorder='big')

        #print de erro do tamanho do head com payload
        if headlen != len(payload2):
            print("ERRO!!! TAMANHO INFORMADO NO HEAD NÃO CONDIZ COM PAYLOAD")
            
        return(head,payload2)


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""


