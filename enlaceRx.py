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

    def getNData(self,size):
        """ Read N bytes of data from the reception buffer
        This function blocks until the number of bytes is received
        """
        return(self.getBuffer(size))


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""
    
    def desfaz_package(self, package):
        #Faz o desempacotamento dos dados baseado-se no protocolo GOOD.
        #Separa o payload do restante e verifica se o tamanho do payload esta correto

        #head(numero do pacote, total de pacotes, erro/pacote esperado, size do payload(3), CRC(3), tipo da msg)

        head_size = 10
        erro = 51
        byte_stuff = bytes.fromhex("FF AA FE FD FC")
        eop = bytes.fromhex("FF FE FD FC")

        payload_size = int.from_bytes(package[3:6], byteorder = "big")

        head = package[0:10]
        #print('head',head)
        package = package[10:]  #pacote sem o head (payload+eop)
        #print('package',package)

        #head_payload = head[7:] #parte do head que representa o size do payload
        #payload_size = int.from_bytes(head_payload, byteorder = "big")  #size do payload

        check = package.find(eop)

        if (check!=-1): #caso o eop seja encontrado
            payload = package[:check] #apenas o payload
            payload = payload.replace(byte_stuff, eop) #retira o bytestuff

            if (len(payload) == payload_size): #se o tamanho indicado no head corresponde ao tamanho real
                return (head+payload)
            else: #caso os tamanhos sejam diferentes
                print('--------------------')
                print("ERRO! Número de Bytes do Payload diferentes do informado no HEAD. Tamanho do payload recebido:{0}".format(len(payload)))
                print("Tamanho do payload esperado:{0}".format(payload_size))
                print('--------------------')
                erro = 51
                return erro

        else: #caso eop nao seja encontrado
            print('--------------------')
            print("ERRO! EOP não encontrado")
            print('--------------------')
            erro = 51
            return erro

